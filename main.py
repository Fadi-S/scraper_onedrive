import asyncio
from azure.identity import InteractiveBrowserCredential
from msgraph import GraphServiceClient
import webbrowser
import httpx

tenant_id = "eaf624c8-a0c4-4195-87d2-443e5d7516cd"
client_id = "2ea0db6a-7212-4998-8f0e-e2fab4ad1ecd"

AUTHORITY_URL = 'https://login.microsoftonline.com/{}'.format(tenant_id)
RESOURCE_URL = 'https://graph.microsoft.com/v1.0/me/drive/root'
redirect_uri = "http://localhost:8080/auth/callback"
API_VERSION = 'v1.0'
scopes = ['Files.ReadWrite.All']
auth = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&scope={'%20'.join(scopes)}"
# webbrowser.open(auth)

credential = InteractiveBrowserCredential(client_id=client_id, tenant_id=tenant_id, redirect_uri=redirect_uri)
access_token = credential.get_token(' '.join(scopes))

print(access_token)

async def main():
    headers = {"Authorization": f"Bearer {access_token.token}"}

    async with httpx.AsyncClient(headers=headers) as http_client:
        folder_name = "NewFolder"
        payload = {
            "name": folder_name,
            "folder": {}
        }
        response = await http_client.post(f"{RESOURCE_URL}:/deep_learning", json=payload)

        if response.status_code == 201:
            print(f"Folder '{folder_name}' created successfully in OneDrive.")
        else:
            print(f"Failed to create folder in OneDrive. Status code: {response.status_code}, Error: {response.json()}")


asyncio.run(main())
