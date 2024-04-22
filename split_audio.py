import os
import json
from pydub import AudioSegment
import csv
from tqdm import tqdm
import random
import string

export_path = "data/splitted_audio"
os.makedirs(export_path, exist_ok=True)


def generate_random_string(length=6):
    characters = string.ascii_letters + string.digits

    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string


done = []
try:
    with open("data/done.json", "r") as file:
        done = json.load(file)
except FileNotFoundError:
    pass

index = 1
index_path = f'{export_path}/index.csv'
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
            filename = generate_random_string()
            start = line["start"]
            end = start + line["duration"]
            # Split audio with python
            split_audio = audio[start * 1000:end * 1000]
            new_path = f"{export_path}/{filename}.mp3"
            split_audio.export(new_path, format="mp3")

            data.append([f"{filename}.mp3", line["text"], gender])

        with open(index_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        done.append(folder)

        with open("data/done.json", "w") as f:
            json.dump(done, f, indent=1)
