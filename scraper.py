import asyncio
import httpx
from get_token import get_token
from helpers import upload_file_to_onedrive, RESOURCE_URL

token = get_token()

success = upload_file_to_onedrive(
    token,
    "keys_example.json",
    "me/drive/root:/deep_learning",
    "keys_example.json"
)

if success:
    print("File uploaded successfully")


async def main():
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(headers=headers) as http_client:
        response = await http_client.get(f"{RESOURCE_URL}/me/drive/root:/deep_learning")

        print(response.json())


asyncio.run(main())
