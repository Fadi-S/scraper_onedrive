import os
import json
from pydub import AudioSegment

data = []

export_path = "data/splitted_audio"

done = json.load(open("data/done.json", "r"))

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
    with open("data/done.json", "w") as f:
        json.dump(data, f, indent=1)
