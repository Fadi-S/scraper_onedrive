import httpx
import os
from tqdm import tqdm
import base64

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

    @staticmethod
    def _list_all_files(source_path):
        file_list = []

        if os.path.isfile(source_path):
            file_list.append(source_path)
        elif os.path.isdir(source_path):
            # If source_path is a directory, recursively list all files inside
            for root, _, files in os.walk(source_path):
                for file_name in files:
                    # Construct relative path of the file
                    relative_path = os.path.relpath(os.path.join(root, file_name).__str__(), source_path)
                    file_list.append(relative_path)

        return file_list

    def upload_folder(self, folder_path, one_drive_folder, skip=None, batch_size=200):
        if skip is None:
            skip = []
        # List all files and directories in the local folder
        items = self._list_all_files(folder_path)
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        count = 0
        batch_requests = []
        # Upload each item in the folder
        for item in tqdm(items):
            item_path = os.path.join(folder_path, item)
            item_name = os.path.basename(item_path)
            if item_path in skip:
                continue

            with open(item_path, "rb") as file:
                file_content = base64.b64encode(file.read()).decode('utf-8')

            batch_requests.append({
                "id": str(count),
                "method": "PUT",
                "url": f"{one_drive_folder}/{item_name}:/content",
                "headers": {
                    "Content-Type": "application/octet-stream"
                },
                "body": file_content
            })

            count += 1
            if count % batch_size == 0:
                batch_payload = {
                    "requests": batch_requests
                }
                response = httpx.post(RESOURCE_URL + "/$batch", headers=headers, json=batch_payload)

                if response.status_code == 200:
                    pass
                else:
                    print(
                        f"Failed to execute batch request. Status code: {response.status_code}, Error: {response.text}")

                batch_requests = []

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
