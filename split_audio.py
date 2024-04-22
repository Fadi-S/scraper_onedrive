import os
import json
from pydub import AudioSegment
import csv
from tqdm import tqdm

export_path = "data/splitted_audio"
os.makedirs(export_path, exist_ok=True)

done = []
try:
    with open("data/done.json", "r") as file:
        done = json.load(file)
except FileNotFoundError:
    pass

index = 1
for gender in ["male", "female"]:
    folders = os.listdir(f"data/{gender}")

    for folder in tqdm(folders):
        if folder in done:
            continue
        path = f"data/{gender}/{folder}"
        audio_path = f"{path}/audio.mp3"
        transcript_path = f"{path}/transcript.json"

        transcript = json.load(open(transcript_path, "r"))
        audio = AudioSegment.from_file(audio_path)
        data = []

        for line in tqdm(transcript):
            start = line["start"]
            end = start + line["duration"]
            # Split audio with python
            split_audio = audio[start * 1000:end * 1000]
            new_path = f"{export_path}/{index}.mp3"
            split_audio.export(new_path, format="mp3")

            data.append([new_path, line["text"], gender])
            index += 1

        file_path = f'{export_path}/index.csv'
        file_exists = os.path.isfile(file_path)
        with open(file_path, 'a' if file_exists else 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        done.append(folder)

        with open("data/done.json", "w") as f:
            json.dump(done, f, indent=1)
