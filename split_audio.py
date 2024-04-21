import os
import json
from pydub import AudioSegment
import csv

data = []

export_path = "data/splitted_audio"
os.makedirs(export_path, exist_ok=True)

done = []
try:
    with open("data/done.json", "r") as file:
        done = json.load(file)
except FileNotFoundError:
    pass

index = 1
try:
    for gender in ["male", "female"]:
        folders = os.listdir(f"data/{gender}")

        for folder in folders:
            if folder in done:
                continue
            path = f"data/{gender}/{folder}"
            audio_path = f"{path}/audio.mp3"
            transcript_path = f"{path}/transcript.json"

            transcript = json.load(open(transcript_path, "r"))
            for line in transcript:
                start = line["start"]
                end = start + line["duration"]
                # Split audio with python
                audio = AudioSegment.from_file(audio_path)
                audio = audio[start * 1000:end * 1000]
                new_path = f"{export_path}/{index}.mp3"
                audio.export(new_path, format="mp3")

                data.append({
                    "audio": new_path,
                    "text": line["text"],
                    "gender": gender,
                })
                index += 1
            done.append(folder)
finally:
    file_path = f'{export_path}/index.csv'
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a' if file_exists else 'w', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['Audio', 'Text', 'Gender'])

        writer.writerows(data)

    with open("data/done.json", "w") as f:
        json.dump(done, f, indent=1)
