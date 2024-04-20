from pytube import Playlist
from pytube import YouTube
from pydub import AudioSegment
import os
import ssl
import uuid

ssl._create_default_https_context = ssl._create_unverified_context

data_path = "data/"
trimmed_path = data_path + "trimmed/"


def download_video(url):
    try:
        filename = str(uuid.uuid4().hex)
        video = YouTube(url)
        stream = video.streams.filter(only_audio=True).first()
        file_path = stream.download(filename=f"{data_path + filename}.mp4")
        print(f"{video.title} is downloaded in WAV format")
        try:
            audio = AudioSegment.from_file(file_path, format="mp4")
        except FileNotFoundError:
            print("Error: File not found")
            return
        if len(audio) < 6 * 60 * 1000:
            print("The audio is less than 6 minutes long.")
            os.remove(file_path)
            return
        start_time = 3 * 60 * 1000  # Convert 3 minutes to milliseconds
        end_time = len(audio) - (3 * 60 * 1000)
        trimmed_audio = audio[start_time:end_time]
        trimmed_file_path = f"{filename}_trimmed.wav"
        if not os.path.exists(trimmed_path):
            os.makedirs(trimmed_path)
        trimmed_audio.export(trimmed_path + trimmed_file_path, format="wav")
        print(f"Trimmed audio saved as {trimmed_file_path}")
    except KeyError:
        print("Unable to fetch video information. Please check the video URL or your network connection.")


URL_PLAYLIST = "https://www.youtube.com/playlist?list=PLRCzrSHS5u_HI0wKuSGdDEmiUQEfrTFZM"

# Retrieve URLs of videos from playlist
playlist = Playlist(URL_PLAYLIST)
print('Number Of Videos In playlist: %s' % len(playlist.video_urls))

urls = []
for url in playlist:
    urls.append(url)
    # download_video(url)

for i, url in enumerate(urls):
    print(f"Downloading video {i + 1} of {len(urls)}")
    print(url)
    download_video(url)
    print("\n\n")
