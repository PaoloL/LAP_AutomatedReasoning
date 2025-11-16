from cedarpy import is_authorized, AuthzResult, Decision
import json

# Load schema from JSON file
with open('schema.json', 'r') as f:
    my_schema = json.load(f)
schema = my_schema

# Load entities from JSON file
with open('entities.json', 'r') as f:
    my_entities = json.load(f)
entities = my_entities

# Define Policies: These define the rules for authorization.
policies: str = """
permit (
    principal in Recube::MyApp::Roles::"Viewer",
    action in [Recube::MyApp::Action::"getBike", Recube::MyApp::Action::"getCars"],
    resource
);

// Grant all access to members of the "Admins" group
permit (
    principal in Recube::MyApp::Roles::"Admin",
    action,
    resource
);
"""

# Define Request: This defines the specific authorization request being made.
denied_request = {
    "principal": "Recube::MyApp::User::\"uid-124\"",
    "action": "Recube::MyApp::Action::\"createBike\"",
    "resource": "Recube::MyApp::Bike::\"vin-123\"" ,
    "context": {
        "ip_address": "127.0.0.1"
    }
}

allowed_request = {
    "principal": "Recube::MyApp::User::\"uid-123\"",
    "action": "Recube::MyApp::Action::\"createBike\"",
    "resource": "Recube::MyApp::Bike::\"vin-123\"" ,
    "context": {
        "ip_address": "127.0.0.1"
    }
}
request = allowed_request
# Evaluate the Request against Policy
authz_result: AuthzResult = is_authorized(allowed_request, policies, entities, schema)

if  authz_result['allowed']:
    print("Authorization Allowed")
else: print("Authorization Denied")
