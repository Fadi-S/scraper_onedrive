from get_token import get_token
from onedrive import OneDrive
import os
import json


token = get_token()
onedrive = OneDrive(token)


uploaded_files = []
if os.path.exists("uploaded_files.json"):
    with open("uploaded_files.json", "r") as file:
        uploaded_files = json.load(file)
else:
    uploaded = onedrive.list_files("me/drive/root:/deep_learning/data/splitted_audio")
    uploaded_files = [os.path.join("data/splitted_audio/", file['name']) for file in uploaded]
    # Save the list of uploaded files to avoid re-uploading
    with open("uploaded_files.json", "w") as file:
        json.dump(uploaded_files, file)
# uploaded_files = []

success = onedrive.upload_folder(
    "data/splitted_audio",
    "me/drive/root:/deep_learning/data/splitted_audio",
    skip=uploaded_files
)

print("Uploaded folder successfully")
