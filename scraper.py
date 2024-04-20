from get_token import get_token
from onedrive import OneDrive

token = get_token()
onedrive = OneDrive(token)

# success = onedrive.upload_file(
#     "keys_example.json",git
#     "me/drive/root:/deep_learning",
#     "keys_example.json"
# )
#
# if success:
#     print("File uploaded successfully")

print("Listing files:")
files = onedrive.list_files("me/drive/root:/deep_learning")
for file in files:
    print(file)
