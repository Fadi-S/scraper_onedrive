import asyncio
from azure.identity import InteractiveBrowserCredential
from msgraph import GraphServiceClient
import webbrowser
import httpx
import json
import time

keys = json.load(open("keys.json"))
tenant_id = keys["tenant"]
client_id = keys["client"]

AUTHORITY_URL = 'https://login.microsoftonline.com/{}'.format(tenant_id)
API_VERSION = 'v1.0'
RESOURCE_URL = f'https://graph.microsoft.com/{API_VERSION}'
redirect_uri = "http://localhost:8080/auth/callback"
scopes = ['Files.ReadWrite.All']
request_auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&scope={'%20'.join(scopes)}"
# webbrowser.open(request_auth_url)

try:
    token = json.load(open("access_token.json"))
    if token["expires_on"] < time.time():
        raise Exception("Token expired")
    access_token = token["token"]
except:
    credential = InteractiveBrowserCredential(client_id=client_id, tenant_id=tenant_id, redirect_uri=redirect_uri)
    access_token = credential.get_token(' '.join(scopes))
    with open("access_token.json", "w") as f:
        f.write(json.dumps({"token": access_token.token, "expires_on": access_token.expires_on}))
    access_token = access_token.token


async def main():
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient(headers=headers) as http_client:
        response = await http_client.get(f"{RESOURCE_URL}/me/drive/root:/deep_learning")

        print(response.json())


asyncio.run(main())
