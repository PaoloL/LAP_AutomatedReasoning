import json
import urllib.parse
from authlib.integrations.requests_client import OAuth2Session


# Environment variables (replace with your own values or set in Lambda)
CLIENT_ID = "1ermt5oepp0efg678vmp749pmm"
CLIENT_SECRET = "1recotmk39bm7t9mfrlvfv52kp6hjf5d7mktj8tfqjq79ocein28"
REDIRECT_URI = "https://vtewj5hzkd.execute-api.eu-west-1.amazonaws.com/prd/callback"
TOKEN_URL = "https://eu-west-1tbppju6ji.auth.eu-west-1.amazoncognito.com/oauth2/token"
USERINFO_URL = "https://eu-west-1tbppju6ji.auth.eu-west-1.amazoncognito.com/oauth2/userInfo"
INDEX_URL = "http://localhost:3000/index2.html"

def lambda_handler(event, context):
    # Extract the authorization code from query parameters
    print("LOG - Event: ", event)
    print("LOG - Context ", context)
   
    try:
        query_params = event.get("queryStringParameters", {})
        code = query_params.get("code")

        if not code:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing code parameter"})
            }

       # Exchange Code with Token and get User Info
        print("LOG - Code: ", code)
        oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)

        # Exchange code for tokens
        token_response = oauth.fetch_token(TOKEN_URL, code=code, grant_type="authorization_code")
        print("LOG - Token: ", token_response)
        oauth.token = token_response
        userinfo = oauth.get(USERINFO_URL).json()
        print("LOG - User Info: ", userinfo)

        # Prepare the response with token and user information
        params = {
            "token": token_response["id_token"],
            "username": userinfo.get("email", "user")
        }

        return {
            "statusCode": 302,
            "headers": {
                "Location": INDEX_URL + "?" + urllib.parse.urlencode(params)
            },
            "body": json.dumps(userinfo)
        }

    except Exception as e:
        print("LOG - Error occurred:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }