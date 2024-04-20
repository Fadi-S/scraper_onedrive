from pytube import Playlist
from download_from_youtube import video_id_from_url
import json
from onedrive import OneDrive
from get_token import get_token

playlist = "https://www.youtube.com/playlist?list=PLRCzrSHS5u_HI0wKuSGdDEmiUQEfrTFZM"

downloaded = json.load(open("urls.json"))["downloaded"]
playlist = Playlist(playlist)

onedrive = OneDrive(get_token())

to_be_deleted = []
for video_link in playlist:
    video_id = video_id_from_url(video_link)
    if video_id in downloaded:
        to_be_deleted = "me/drive/root:/deep_learning/data/" + downloaded[video_id]["gender"] + "/" + downloaded[video_id]["path"]
        onedrive.delete_item(to_be_deleted)
