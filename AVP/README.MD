# Amazon Verified Permissions (AVP) Demo

## Overview

This demo showcases Amazon Verified Permissions (AVP), a managed service that provides fine-grained authorization using Cedar policies. AVP integrates with AWS services to provide scalable, centralized authorization for applications.

## Setup

### Prerequisites
- AWS CLI configured with appropriate permissions
- AWS SAM CLI installed
- Python 3.8+ for Lambda functions

### Architecture
This demo deploys a complete authorization system including:
- **Amazon Cognito** - User authentication and group management
- **Amazon Verified Permissions** - Policy store with Cedar policies
- **API Gateway** - REST API with Lambda authorizer
- **Lambda Functions** - Authorization logic and API handlers

## SAM Build and Deploy

### 1. Build the Application
```bash
cd AVP/
sam build
```

### 2. Deploy with Guided Setup
```bash
sam deploy --guided
```

During guided deployment, you'll configure:
- Stack name
- AWS region
- Parameter values
- IAM role creation confirmation

### 3. Infrastructure Created
The CloudFormation stack creates:
- **Cognito User Pool** with admin and viewer groups
- **AVP Policy Store** with Cedar schema and policies
- **API Gateway** with Lambda authorizer integration
- **Lambda Functions** for authorization and callback handling

## Demo Testing

### 1. Get Authentication Token
```bash
# Use values from stack outputs
USER_POOL_ID="your-user-pool-id"
CLIENT_ID="your-client-id"
USERNAME="admin@example.com"
PASSWORD="TempPassword123!"

# Get ID token
aws cognito-idp admin-initiate-auth \
  --user-pool-id $USER_POOL_ID \
  --client-id $CLIENT_ID \
  --auth-flow ADMIN_NO_SRP_AUTH \
  --auth-parameters USERNAME=$USERNAME,PASSWORD=$PASSWORD
```

### 2. Test API Authorization
```bash
API_URL="https://your-api-id.execute-api.region.amazonaws.com/prd"
TOKEN="your-id-token"

# Test GET /bikes (allowed for admin and viewer)
curl -X GET "$API_URL/bikes" \
  -H "Authorization: Bearer $TOKEN"

# Test POST /bikes (allowed only for admin)
curl -X POST "$API_URL/bikes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"brand": "Trek", "model": "FX3"}'

# Test without token (should be denied)
curl -X GET "$API_URL/bikes"
```

### Expected Results
- **Admin users:** Full CRUD operations (GET, POST, PUT, DELETE)
- **Viewer users:** Read-only operations (GET only)
- **Unauthenticated requests:** Denied with 401/403 status

## Key Takeaways

- **Managed Service:** AVP provides scalable, managed authorization without infrastructure overhead
- **Cedar Integration:** Leverages Cedar's mathematical reasoning for policy decisions
- **AWS Integration:** Seamlessly integrates with Cognito, API Gateway, and Lambda
- **Fine-grained Control:** Supports complex authorization scenarios with attribute-based policies
- **Centralized Policies:** Single policy store for multiple applications and services
- **Real-time Decisions:** Sub-millisecond authorization decisions at scale
- **Audit and Compliance:** Built-in logging and monitoring for authorization decisions

## Cleanup
```bash
sam delete
```

## Additional Resources
- [Amazon Verified Permissions Documentation](https://docs.aws.amazon.com/verifiedpermissions/)
- [Cedar Policy Language Guide](https://docs.cedarpolicy.com/)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
