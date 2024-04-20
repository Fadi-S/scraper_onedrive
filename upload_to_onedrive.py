from get_token import get_token
from onedrive import OneDrive

token = get_token()
onedrive = OneDrive(token)

success = onedrive.upload_folder(
    "data",
    "me/drive/root:/deep_learning/data"
)

print("Uploaded folder successfully")