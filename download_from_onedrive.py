from get_token import get_token
from onedrive import OneDrive

token = get_token()
onedrive = OneDrive(token)

success = onedrive.download_folder(
    "data/male",
    "me/drive/root:/deep_learning/data/Original/male"
)

print("Folder downloaded successfully")
