from get_token import get_token
from onedrive import OneDrive

token = get_token()
onedrive = OneDrive(token)

success = onedrive.download_folder(
    "data",
    "me/drive/root:/deep_learning/data/Original"
)

print("Folder downloaded successfully")
