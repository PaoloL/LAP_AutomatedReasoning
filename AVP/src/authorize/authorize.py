import os
import json
import base64
import boto3

vp_client = boto3.client(
    "verifiedpermissions",
    endpoint_url=(
        f"https://{os.environ['ENDPOINT']}ford.{os.environ['AWS_REGION']}.amazonaws.com"
        if os.environ.get("ENDPOINT")
        else None
    )
)

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
    try:
        # Get bearer token from headers
        headers = event.get("headers", {})
        bearer_token = headers.get("authorization") or headers.get("Authorization")

        if bearer_token and bearer_token.lower().startswith("bearer "):
            bearer_token = bearer_token.split(" ")[1]

        if not bearer_token:
            raise Exception("Missing bearer token")

        # Parse token
        parsed_token = parse_token(bearer_token)

        # Construct actionId from HTTP method and path
        method = event["requestContext"]["httpMethod"].lower()
        path = event["requestContext"]["resourcePath"]
        action_id = f"{method} {path}"

        # Build authorization request
        auth_input = {
            TOKEN_TYPE: bearer_token,
            "policyStoreId": POLICY_STORE_ID,
            "action": {
                "actionType": ACTION_TYPE,
                "actionId": action_id,
            },
            "resource": {
                "entityType": RESOURCE_TYPE,
                "entityId": RESOURCE_ID
            },
            "context": get_context_map(event),
        }

        # Call Verified Permissions
        auth_response = vp_client.is_authorized_with_token(**auth_input)
        decision = auth_response["decision"]

        # Determine principal ID
        principal_id = f"{parsed_token['iss'].split('/')[-1]}|{parsed_token['sub']}"
        if "principal" in auth_response:
            principal = auth_response["principal"]
            principal_id = f"{principal['entityType']}::\"{principal['entityId']}\""

        return {
            "principalId": principal_id,
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow" if decision.upper() == "ALLOW" else "Deny",
                        "Resource": event["methodArn"]
                    }
                ]
            },
            "context": {
                "actionId": action_id
            }
        }

    except Exception as e:
        print("Authorization error:", str(e))
        return {
            "principalId": "",
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
            "context": {}
        }

