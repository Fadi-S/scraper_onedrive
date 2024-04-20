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
videos_path = data_path + "videos/"
formatter = JSONFormatter()

if not os.path.exists(videos_path):
    os.makedirs(videos_path)

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
    try:
        file_path = stream.download(filename=f"{videos_path + filename}.mp4")
    except Exception as e:
        print(f"Error downloading {video_id}: {e}\n")
        return
    print(f"{video_id} downloaded")

    audio = AudioSegment.from_file(file_path, format="mp4")
    audio_path = f"{path}/audio.wav"
    transcript_path = f"{path}/transcript.json"

    bitrate = "64k"
    sample_rate = 44100
    compression = "pcm_s16le"  # PCM compression for lossless quality

    audio.export(audio_path, format="wav", bitrate=bitrate,
                 parameters=["-ar", str(sample_rate), "-ac", "1", "-acodec", compression])
    print(f"Audio saved as {audio_path}")

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

