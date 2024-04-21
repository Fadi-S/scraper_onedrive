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

        download_url = f"{RESOURCE_URL}/{one_drive_file}"
        response = httpx.get(download_url, headers=headers, follow_redirects=True)

        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            return True
        else:
            print(f"Failed to download file. Status code: {response.status_code}, Error: {response.text}")
            return False

    def download_folder(self, local_folder_path, one_drive_folder):
        # Create the local folder if it doesn't exist
        os.makedirs(local_folder_path, exist_ok=True)

        # List files and folders in the OneDrive folder
        items = self.list_files(one_drive_folder)

        if items is None:
            print(f"Failed to list files in folder: {one_drive_folder}")
            return

        # Download each item in the folder
        for item in tqdm(items):
            item_name = item['name']
            item_type = 'folder' if 'folder' in item else 'file'

            # If the item is a file, download it
            if item_type == 'file':
                item_id = item['id']
                local_file_path = os.path.join(local_folder_path, item_name)
                self.download_file(local_file_path, f"me/drive/items/{item_id}/content")

            # If the item is a folder, recursively download its contents
            elif item_type == 'folder':
                subfolder_name = item_name
                subfolder_path = os.path.join(local_folder_path, subfolder_name)
                self.download_folder(subfolder_path, f"{one_drive_folder}/{subfolder_name}")

    def list_files(self, one_drive_folder):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        list_url = f"{RESOURCE_URL}/{one_drive_folder}:/children"
        all_items = []

        while list_url:
            response = httpx.get(list_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                items = data.get('value', [])
                all_items.extend(items)
                list_url = data.get('@odata.nextLink')
            else:
                print(f"Failed to list files. Status code: {response.status_code}, Error: {response.text}")
                return None

        return all_items

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

    def delete_item(self, path):
        # Construct the URL for the item to delete
        delete_url = f"{RESOURCE_URL}/{path}"

        # Set up the request headers with the authorization token
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        # Send the DELETE request to delete the item
        response = httpx.delete(delete_url, headers=headers)

        # Check if the deletion was successful
        if response.status_code == 204:
            return True
        else:
            print(f"Failed to delete item at path: {path}. Status code: {response.status_code}, Error: {response.text}")
            return False
