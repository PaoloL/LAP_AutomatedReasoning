from cedarpy import is_authorized, AuthzResult, Decision

# Policies: These define the rules for authorization.
policies: str = """
permit(
    principal == User::"bob",
    action == Action::"view",
    resource == Photo::"1234-abcd"
);
"""

# Entities: These represent the principals, resources, and actions in your system.
entities: list = [  # a list of Cedar entities; can also be a json-formatted string of Cedar entities
    {"uid": {"__entity": { "type" : "User", "id" : "alice" }}, "attrs": {}, "parents": []}
    # ...
]

# Request: This defines the specific authorization request being made.
request = {
    "principal": 'User::"bob"',
    "action": 'Action::"view"',
    "resource": 'Photo::"1234-abcd"',
    "context": {} # Context: Additional data about the request that can be used in policies.
}

# Schema: the schema defines the types and relationships of entities and attributes, and is used for validation.
schema = my_schema


authz_result: AuthzResult = is_authorized(request, policies, entities, my_schema)

assert authz_result['allowed']
print(authz_result['decision'])