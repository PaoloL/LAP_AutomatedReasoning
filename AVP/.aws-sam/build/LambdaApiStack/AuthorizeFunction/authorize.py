import os
import json
import base64
import boto3

vp_client = boto3.client("verifiedpermissions")

POLICY_STORE_ID = os.environ["POLICY_STORE_ID"]
NAMESPACE = os.environ["NAMESPACE"]
TOKEN_TYPE = os.environ["TOKEN_TYPE"]
RESOURCE_TYPE = f"{NAMESPACE}::Application"
RESOURCE_ID = NAMESPACE
ACTION_TYPE = f"{NAMESPACE}::Action"


def parse_token(token):
    """Decode JWT payload"""
    payload = token.split('.')[1]
    padded = payload + '=' * (4 - len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(padded))


def get_context_map(event):
    context_map = {}

    if event.get("pathParameters"):
        context_map["pathParameters"] = {
            "record": {
                k: {"string": v} for k, v in event["pathParameters"].items()
            }
        }

    if event.get("queryStringParameters"):
        context_map["queryStringParameters"] = {
            "record": {
                k: {"string": v} for k, v in event["queryStringParameters"].items()
            }
        }

    if not context_map:
        return None

    return {"contextMap": context_map}


def lambda_handler(event, context):
    print(f"DEBUG: Received event: {json.dumps(event, default=str)}")
    print(f"DEBUG: Environment - POLICY_STORE_ID: {POLICY_STORE_ID}")
    print(f"DEBUG: Environment - NAMESPACE: {NAMESPACE}")
    print(f"DEBUG: Environment - TOKEN_TYPE: {TOKEN_TYPE}")
    
    try:
        # Get bearer token from headers
        headers = event.get("headers", {})
        print(f"DEBUG: Headers: {headers}")
        
        bearer_token = headers.get("authorization") or headers.get("Authorization")
        print(f"DEBUG: Bearer token found: {bool(bearer_token)}")

        if bearer_token and bearer_token.lower().startswith("bearer "):
            bearer_token = bearer_token.split(" ")[1]
            print(f"DEBUG: Extracted token (first 20 chars): {bearer_token[:20]}...")

        if not bearer_token:
            print("DEBUG: No bearer token found")
            raise Exception("Missing bearer token")

        # Parse token
        parsed_token = parse_token(bearer_token)
        print(f"DEBUG: Parsed token: {parsed_token}")

        # Construct actionId from HTTP method and path
        method = event["requestContext"]["httpMethod"].lower()
        path = event["requestContext"]["resourcePath"]
        action_id = f"{method} {path}"
        print(f"DEBUG: Action ID: {action_id}")
        print(f"DEBUG: Action Type: {ACTION_TYPE}")
        print(f"DEBUG: Resource Type: {RESOURCE_TYPE}")
        print(f"DEBUG: Resource ID: {RESOURCE_ID}")

        # Build authorization request
        auth_input = {
            "policyStoreId": POLICY_STORE_ID,
            "identityToken": bearer_token,
            "action": {
                "actionType": ACTION_TYPE,
                "actionId": action_id,
            },
            "resource": {
                "entityType": RESOURCE_TYPE,
                "entityId": RESOURCE_ID
            }
        }
        
        # Add context if available
        context_map = get_context_map(event)
        if context_map:
            auth_input["context"] = context_map
            print(f"DEBUG: Added context: {context_map}")
        
        print(f"DEBUG: Auth input: {json.dumps(auth_input, default=str)}")

        # Call Verified Permissions
        print("DEBUG: Calling Verified Permissions API...")
        auth_response = vp_client.is_authorized_with_token(**auth_input)
        print(f"DEBUG: Auth response: {auth_response}")
        
        decision = auth_response["decision"]
        print(f"DEBUG: Decision: {decision}")

        # Determine principal ID
        principal_id = f"{parsed_token['iss'].split('/')[-1]}|{parsed_token['sub']}"
        if "principal" in auth_response:
            principal = auth_response["principal"]
            principal_id = f"{principal['entityType']}::\"{principal['entityId']}\""
        
        print(f"DEBUG: Principal ID: {principal_id}")
        
        effect = "Allow" if decision.upper() == "ALLOW" else "Deny"
        print(f"DEBUG: Policy effect: {effect}")

        return {
            "principalId": principal_id,
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": effect,
                        "Resource": event["methodArn"]
                    }
                ]
            },
            "context": {
                "actionId": action_id
            }
        }

    except Exception as e:
        print(f"DEBUG: Authorization error occurred: {str(e)}")
        print(f"DEBUG: Error type: {type(e).__name__}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        
        return {
            "principalId": "error",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Deny",
                        "Resource": event["methodArn"]
                    }
                ]
            },
            "context": {
                "error": str(e)
            }
        }

