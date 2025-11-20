#!/usr/bin/env python3
"""
Amazon Bedrock Guardrails Demo - Travel Assistant
Demonstrates automated reasoning capabilities through Bedrock Guardrails
"""

import boto3
import json
from botocore.exceptions import ClientError

# Configuration
MODEL_ID = "eu.amazon.nova-micro-v1:0"
GUARDRAIL_ID = "spi7qw5ij0ch"
GUARDRAIL_VERSION = "DRAFT"
REGION = "eu-west-1"

# System prompt for travel assistant
SYSTEM_PROMPT = """You are a helpful travel assistant. 
You provide Hotels recommendations based on cirty and budget.
You should answer only with a list of 5 hotels in the requested city"""

# Test scenarios - one that might trigger guardrails
TEST_SCENARIOS_OK = {
        "name": "In-Policy Travel Query",
        "message": "Can you propose the best Hotel in Rome inside a budget of 100 Eur ?"
    }

TEST_SCENARIOS_KO = {
        "name": "Off-Policy Travel Query",
        "message": "Can you propose the best Hotel in Boston inside a budget of 100 Eur ?"    }

def create_bedrock_client():
    """Create Bedrock Runtime client"""
    return boto3.client('bedrock-runtime', region_name=REGION)

def invoke_model_without_guardrails(client, user_message):
    """Invoke Nova Micro without guardrails"""
    try:
        messages = [
            {
                "role": "user",
                "content": [{"text": f"{SYSTEM_PROMPT}\n\nUser: {user_message}"}]
            }
        ]
        
        response = client.converse(
            modelId=MODEL_ID,
            messages=messages,
            inferenceConfig={
                "maxTokens": 500,
                "temperature": 0.7
            }
        )
        
        return {
            "success": True,
            "content": response['output']['message']['content'][0]['text'],
            "stop_reason": response.get('stopReason', 'end_turn')
        }
        
    except ClientError as e:
        return {
            "success": False,
            "error": str(e)
        }

def invoke_model_with_guardrails(client, user_message):
    """Invoke Nova Micro with guardrails enabled"""
    try:
        messages = [
            {
                "role": "user", 
                "content": [{"text": f"{SYSTEM_PROMPT}\n\nUser: {user_message}"}]
            }
        ]
        
        response = client.converse(
            modelId=MODEL_ID,
            messages=messages,
            inferenceConfig={
                "maxTokens": 500,
                "temperature": 0.7
            },
            guardrailConfig={
                "guardrailIdentifier": GUARDRAIL_ID,
                "guardrailVersion": GUARDRAIL_VERSION
            }
        )
        
        return {
            "success": True,
            "content": response['output']['message']['content'][0]['text'],
            "stop_reason": response.get('stopReason', 'end_turn'),
            "guardrail_action": response.get('guardrailAction', 'NONE')
        }
        
    except ClientError as e:
        if 'GuardrailException' in str(e):
            return {
                "success": False,
                "blocked": True,
                "error": "Content blocked by guardrails",
                "details": str(e)
            }
        return {
            "success": False,
            "error": str(e)
        }

def run_demo():
    """Run the complete Bedrock Guardrails demo"""
    print("Amazon Bedrock Guardrails Demo - Travel Assistant")
    print("This demo shows automated reasoning through Bedrock Guardrails")

    
    # Initialize Bedrock client
    try:
        client = create_bedrock_client()
        print("Successfully connected to Amazon Bedrock")
    except Exception as e:
        print(f"Failed to connect to Bedrock: {e}")
        return
    
    # Run scenarios without guardrails    
    result_no_guardrails = invoke_model_without_guardrails(client, TEST_SCENARIOS_KO)    
    if result_no_guardrails['success']:
        print("Response received:")
        print(f"Content: {result_no_guardrails['content']}")
        print(f"Stop Reason: {result_no_guardrails['stop_reason']}")
    else:
        print(f"Error: {result_no_guardrails['error']}")
        
    # Run scenarios With Guardrails
    result_with_guardrails = invoke_model_with_guardrails(client, TEST_SCENARIOS_KO)    
    if result_with_guardrails['success']:
        print("Response received:")
        print(f"Content: {result_with_guardrails['content']}")
        print(f"Stop Reason: {result_with_guardrails['stop_reason']}")
        print(f"Guardrail Action: {result_with_guardrails.get('guardrail_action', 'NONE')}")
    else:
        print(f"Error: {result_with_guardrails['error']}")

if __name__ == "__main__":
    run_demo()