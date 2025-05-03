import boto3  
import time  
import json
import botocore

# Initialize clients
bedrock_agent = boto3.client('bedrock-agent', region_name='us-west-2')
iam = boto3.client('iam', region_name='us-west-2')

# Role name - remove the path prefix
role_name = 'AmazonBedrockExecutionRoleForAgents_P89YO45QHD'  # Removed 'service-role/' prefix

# Role ARN - keep the full path for the ARN
role_arn = 'arn:aws:iam::043309322265:role/service-role/AmazonBedrockExecutionRoleForAgents_P89YO45QHD'

# Check if role exists, create if it doesn't
try:
    role_response = iam.get_role(RoleName=role_name)
    print(f"Using existing role: {role_arn}")
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchEntity':
        print(f"Role {role_name} not found. Creating it...")
        
        # Trust policy for Bedrock
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "bedrock.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        # Create the role with path
        role_response = iam.create_role(
            Path='/service-role/',  # Specify the path separately
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="Service role for Amazon Bedrock"
        )
        
        # Attach policy to the role
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonBedrockExecutionRoleForAgents'
        )
        
        # Wait for role to propagate
        print("Waiting for role to propagate...")
        time.sleep(10)
        
        role_arn = role_response['Role']['Arn']
        print(f"Created role with ARN: {role_arn}")
    else:
        raise e

try:  
    # Create the agent with updated parameters
    response = bedrock_agent.create_agent(  
        agentName='agent-quick-start-8tazfID50PJ7J5VA8',  
        description='Intelligent Customer Service Chatbot for Amazon Retail',
        instruction='You are a helpful customer service agent for an online store. Use a step-by-step approach to solve customer problems.',  
        idleSessionTTLInSeconds=600,  
        agentResourceRoleArn=role_arn,  # Use the role ARN variable
        foundationModel='cohere.command-text-v14'
    )  
    agent_id = response['agent']['agentId']  
    print(f"Agent created with ID: {agent_id}")  

    # Wait for the agent to be in 'CREATED' state  
    while True:  
        agent_status = bedrock_agent.get_agent(agentId=agent_id)['agent']['agentStatus']  
        print(f"Agent status: {agent_status}")  
        if agent_status == 'CREATED':  
            break  
        time.sleep(10)
    
    # Define the 5 core intents
    intents = [
        {
            'intentName': 'track_order',
            'description': 'Help customers track their order status',
            'sampleUtterances': [
                {'utterance': "Where's my order?"},
                {'utterance': "I want to track my package"},
                {'utterance': "When will my order arrive?"},
                {'utterance': "What's the status of my order?"},
                {'utterance': "I haven't received my order yet"}
            ],
            'intentResponse': {
                'responseType': 'TEMPLATE',
                'template': "I'll help you track your order. Let me break this down:\n1. First, I need your order ID\n2. I'll check the status in our system\n3. I'll provide you with the current status and estimated delivery date\n\nCould you please provide your order ID?"
            }
        },
        {
            'intentName': 'return_item',
            'description': 'Process item returns for customers',
            'sampleUtterances': [
                {'utterance': "I want to return something I bought"},
                {'utterance': "How do I return an item?"},
                {'utterance': "Return policy"},
                {'utterance': "I need to send back a product"},
                {'utterance': "Can I get a refund?"}
            ],
            'intentResponse': {
                'responseType': 'TEMPLATE',
                'template': "I can help you return your item. Here's the process:\n1. Verify your order details\n2. Determine eligibility for return\n3. Generate a return label\n4. Process your refund once received\n\nCould you share your order number and the item you wish to return?"
            }
        },
        {
            'intentName': 'product_info',
            'description': 'Provide information about products',
            'sampleUtterances': [
                {'utterance': "Tell me more about this product"},
                {'utterance': "What are the specifications?"},
                {'utterance': "Is this item in stock?"},
                {'utterance': "Do you have this in other colors?"},
                {'utterance': "What's the warranty on this?"}
            ],
            'intentResponse': {
                'responseType': 'TEMPLATE',
                'template': "I'd be happy to provide product information. Let me approach this systematically:\n1. Identify the exact product you're interested in\n2. Retrieve the specifications and details\n3. Check availability and options\n\nWhich product would you like to know more about?"
            }
        },
        {
            'intentName': 'cancel_order',
            'description': 'Help customers cancel their orders',
            'sampleUtterances': [
                {'utterance': "I need to cancel my order"},
                {'utterance': "Can I stop my purchase?"},
                {'utterance': "I changed my mind about my order"},
                {'utterance': "Cancel my recent purchase"},
                {'utterance': "How do I cancel an order?"}
            ],
            'intentResponse': {
                'responseType': 'TEMPLATE',
                'template': "I can help you cancel your order. Let's go through this step by step:\n1. Verify your order details\n2. Check if the order is eligible for cancellation\n3. Process the cancellation\n4. Confirm the refund timeline\n\nCould you please provide your order number?"
            }
        },
        {
            'intentName': 'contact_support',
            'description': 'Connect customers with human support',
            'sampleUtterances': [
                {'utterance': "I want to speak to a human"},
                {'utterance': "Connect me with customer service"},
                {'utterance': "Talk to a representative"},
                {'utterance': "I need additional help"},
                {'utterance': "This isn't solving my problem"}
            ],
            'intentResponse': {
                'responseType': 'TEMPLATE',
                'template': "I understand you'd like to speak with our support team. Let me help with that:\n1. I'll need to know what your issue is about\n2. I'll find the right department for you\n3. I'll provide contact options\n\nCould you briefly tell me what you need assistance with?"
            }
        }
    ]
    
    # Add each intent to the agent
    for intent in intents:
        intent_response = bedrock_agent.create_agent_intent(
            agentId=agent_id,
            intentName=intent['intentName'],
            description=intent['description'],
            sampleUtterances=intent['sampleUtterances'],
            intentResponse=intent['intentResponse']
        )
        print(f"Created intent: {intent['intentName']}")
    
    # Create the Agent Alias  
    alias_response = bedrock_agent.create_agent_alias(  
        agentId=agent_id,
        agentAliasName='Production',  
        routingConfiguration=[  
            {  
                'foundationModel': 'cohere.command-text-v14',
                'modelWeight': 1  
            }  
        ]  
    )  
    alias_id = alias_response['agentAlias']['agentAliasId']  
    print(f"Agent Alias created with ID: {alias_id}")
    
    # Prepare the agent for use
    prepare_response = bedrock_agent.prepare_agent(
        agentId=agent_id
    )
    print("Agent preparation initiated")
    
    # Wait for the agent to be prepared
    while True:
        agent_status = bedrock_agent.get_agent(agentId=agent_id)['agent']['agentStatus']
        print(f"Agent preparation status: {agent_status}")
        if agent_status == 'PREPARED':
            break
        time.sleep(10)
    
    print("Agent is ready for testing!")
    print("You can now test the agent with: 'Hello, how can I assist you?'")

except Exception as e:  
    print(f"Error: {e}")
