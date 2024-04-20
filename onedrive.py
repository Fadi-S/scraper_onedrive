import httpx
import os
from tqdm import tqdm
RESOURCE_URL = f'https://graph.microsoft.com/v1.0'


class OneDrive:
    def __init__(self, token):
        self.token = token

    def upload_file(self, file_path, one_drive_folder, file_name):
        headers = {
            "Authorization": f"Bearer {self.token}",
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

    def download_file(self, file_path, one_drive_file):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        download_url = f"{RESOURCE_URL}/{one_drive_file}:/content"
        response = httpx.get(download_url, headers=headers)

        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            return True
        else:
            print(f"Failed to download file. Status code: {response.status_code}, Error: {response.text}")
            return False

    def list_files(self, one_drive_folder):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        list_url = f"{RESOURCE_URL}/{one_drive_folder}:/children"
        response = httpx.get(list_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to list files. Status code: {response.status_code}, Error: {response.text}")
            return None

    def upload_folder(self, folder_path, one_drive_folder):
        # List all files and directories in the local folder
        items = os.listdir(folder_path)

        # Upload each item in the folder
        for item in tqdm(items):
            item_path = os.path.join(folder_path, item)
            item_name = os.path.basename(item_path)

            # If the item is a file, upload it to OneDrive
            if os.path.isfile(item_path):
                if not self.upload_file(item_path, one_drive_folder, item_name):
                    print(f"Failed to upload file: {item_name}")

            # If the item is a directory, recursively upload its contents
            elif os.path.isdir(item_path):
                subfolder = os.path.join(one_drive_folder, item_name)
                self.upload_folder(item_path, subfolder)
