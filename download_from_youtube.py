from pytube import Playlist
from pytube import YouTube
from pydub import AudioSegment
import os
import uuid
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from urllib.parse import urlparse, parse_qs


def video_id_from_url(value):
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None


data_path = "data/"
formatter = JSONFormatter()

urls = json.load(open("urls.json"))
undownloaded = urls["undownloaded"]
downloaded = urls["downloaded"]

decoder = json.decoder.JSONDecoder()


def download_video(url, gender):
    video_id = video_id_from_url(url)
    if video_id in downloaded:
        return

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar'])
    except:
        return

    print(f"Started downloading {video_id}")

    filename = str(uuid.uuid4().hex)
    path = data_path + "processed/" + filename
    if not os.path.exists(path):
        os.makedirs(path)

    video = YouTube(url)
    stream = video.streams.filter(only_audio=True).first()
    audio_path = f"{path}/audio.mp3"
    try:
        stream.download(filename=audio_path)
    except Exception as e:
        print(f"Error downloading {video_id}: {e}\n")
        return
    print(f"{video_id} downloaded as mp3")

    transcript_path = f"{path}/transcript.json"

    transcript_object = decoder.decode(formatter.format_transcript(transcript))

    with open(transcript_path, 'w') as json_file:
        json.dump(transcript_object, json_file, ensure_ascii=False)
    print(f"Transcript file downloaded in {transcript_path}")

    downloaded[video_id] = {
        "id": video_id,
        "path": filename,
        "gender": gender
    }
    print(f"Done video {video_id}\n")


try:
    for url in undownloaded:
        link = url["link"]
        if url["playlist"]:
            playlist = Playlist(link)
            for video_link in playlist:
                download_video(video_link, url["gender"])
        else:
            download_video(link, url["gender"])
        undownloaded.remove(url)
finally:
    with open("urls.json", "w") as file:
        json.dump({
            "downloaded": downloaded,
            "undownloaded": undownloaded,
        }, file, indent=1)

