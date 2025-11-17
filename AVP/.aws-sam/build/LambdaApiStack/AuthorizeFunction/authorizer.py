import os
import json
import base64
import boto3

vp_client = boto3.client("verifiedpermissions")

POLICY_STORE_ID = os.environ["POLICY_STORE_ID"]
NAMESPACE = os.environ["NAMESPACE"]

# HTTP method to Cedar action mapping
ACTION_MAPPING = {
    "GET /bikes": "getAllBikes",
    "POST /bikes": "createBike", 
    "GET /bike/{bikeId}": "getBike",
    "PUT /bike/{bikeId}": "updateBike",
    "DELETE /bike/{bikeId}": "deleteBike",
    "GET /cars": "getAllCars",
    "POST /cars": "createCar",
    "GET /car/{carId}": "getCar",
    "PUT /car/{carId}": "updateCar",
    "DELETE /car/{carId}": "deleteCar"
}

def parse_token(token):
    """Decode JWT payload"""
    payload = token.split('.')[1]
    padded = payload + '=' * (4 - len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(padded))

def getIdentityToken(event):
    """Extract token from request"""
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
    
    return bearer_token

def getActionId(event):
    """Extract ActionId from request"""
    method = event["requestContext"]["httpMethod"]
    path = event["requestContext"]["resourcePath"]
    action_key = f"{method} {path}"
    print(f"DEBUG: Action key: {action_key}")
    
    cedar_action = ACTION_MAPPING.get(action_key)
    print(f"DEBUG: Cedar action: {cedar_action}")
    if not cedar_action:
        raise Exception(f"No Cedar action mapping for {action_key}")
    
    return cedar_action

def getEntityId(event):
    """Extract entityId from Request"""
    path = event["requestContext"]["resourcePath"]
    
    # Determine resource type from path
    if "/bike" in path.lower():
        resource_type = "Bike" 
    elif "/car" in path.lower():
        resource_type = "Car" 
    else:
        raise Exception(f"Unknown resource type for path: {path}")
    
    print(f"DEBUG: Resource type: {resource_type}")
    
    # Get resource ID from path parameters or use collection name
    path_params = event.get("pathParameters") or {}
    resource_id = path_params.get("bikeId") or path_params.get("carId") or resource_type.lower()
    print(f"DEBUG: Path params: {path_params}")
    print(f"DEBUG: Resource ID: {resource_id}")
    
    return resource_type, resource_id

def callAVP(identity_token, action_id, resource_type, entity_id):
    """Put all info together, call Verified Permission and return Allow/Deny Policy"""
    auth_input = {
        "policyStoreId": POLICY_STORE_ID,
        "identityToken": identity_token,
        "action": {
            "actionType": f"{NAMESPACE}::Action",
            "actionId": action_id,
        },
        "resource": {
            "entityType": f"{NAMESPACE}::{resource_type}",
            "entityId": entity_id
        }
    }
    print(f"DEBUG: Auth input: {json.dumps(auth_input, default=str)}")

    # Call Verified Permissions
    print("DEBUG: Calling Verified Permissions API...")
    auth_response = vp_client.is_authorized_with_token(**auth_input)
    print(f"DEBUG: Auth response: {auth_response}")
    
    decision = auth_response["decision"]
    print(f"DEBUG: Decision: {decision}")
    
    effect = "Allow" if decision.upper() == "ALLOW" else "Deny"
    print(f"DEBUG: Policy effect: {effect}")
    
    return effect

def lambda_handler(event, context):
    print(f"DEBUG: Received event: {json.dumps(event, default=str)}")
    print(f"DEBUG: Environment - POLICY_STORE_ID: {POLICY_STORE_ID}")
    print(f"DEBUG: Environment - NAMESPACE: {NAMESPACE}")
    
    try:
        # Extract components using helper functions
        identity_token = getIdentityToken(event)
        action_id = getActionId(event)
        resource_type, entity_id = getEntityId(event)
        
        # Call AVP for authorization decision
        effect = callAVP(identity_token, action_id, resource_type, entity_id)
        
        # Parse token for principal ID
        parsed_token = parse_token(identity_token)
        principal_id = f"{parsed_token['iss'].split('/')[-1]}|{parsed_token['sub']}"
        print(f"DEBUG: Principal ID: {principal_id}")

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
                "cedarAction": action_id
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