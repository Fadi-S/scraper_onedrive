import httpx

RESOURCE_URL = f'https://graph.microsoft.com/v1.0'


def upload_file_to_onedrive(token, file_path, one_drive_folder, file_name):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    with open(file_path, "rb") as file:
        file_content = file.read()

    upload_url = f"{RESOURCE_URL}/{one_drive_folder}/{file_name}:/content"
    response = httpx.put(upload_url, headers=headers, data=file_content)

    if response.status_code == 201:
        return True
    else:
        print(f"Failed to upload file. Status code: {response.status_code}, Error: {response.text}")
        return False