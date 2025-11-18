#### 1. Deploy CloudFormation Stack

Deploy the complete infrastructure stack:

```bash
cd AVP/
sam build
sam deploy --guided
```

The stack creates:
- **Cognito User Pool** with admin and viewer groups
- **AVP Policy Store** with Cedar schema and policies
- **API Gateway** with Lambda authorizer
- **Lambda Functions** for authorization and callback handling

#### 2. Test the API with Curl

After deployment, test the authorization system:

**Get Cognito Token:**
```bash
# Replace with your actual values from stack outputs
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

**Test API Endpoints:**
```bash
# Replace with your API Gateway URL and token
API_URL="https://your-api-id.execute-api.region.amazonaws.com/prd"
TOKEN="your-id-token"

# Test GET /bikes (should work for both admin and viewer)
curl -X GET "$API_URL/bikes" \
  -H "Authorization: Bearer $TOKEN"

# Test POST /bikes (should work only for admin)
curl -X POST "$API_URL/bikes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"brand": "Trek", "model": "FX3"}'

# Test without token (should be denied)
curl -X GET "$API_URL/bikes"
```

**Expected Results:**
- **Admin users:** Can perform all operations (GET, POST, PUT, DELETE)
- **Viewer users:** Can only perform GET operations
- **Unauthenticated requests:** Denied with 401/403 status
