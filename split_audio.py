import os
import json
from pydub import AudioSegment
import csv
from tqdm import tqdm
import threading

# Define a lock for synchronizing access to the index variable
index_lock = threading.Lock()


def process_folder(gender, folder, export_path, done):
    global index

    if folder in done:
        return

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

        # Use the lock to synchronize access to the index variable
        with index_lock:
            new_path = f"{export_path}/{index}.mp3"
            index += 1

        split_audio.export(new_path, format="mp3")

        data.append([new_path, line["text"], gender])

    with open(f'{export_path}/index.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    done.append(folder)


def main():
    export_path = "data/splitted_audio"
    os.makedirs(export_path, exist_ok=True)

    done = []
    try:
        with open("data/done.json", "r") as file:
            done = json.load(file)
    except FileNotFoundError:
        pass

    global index
    index = 1

    threads = []
    for gender in ["male", "female"]:
        folders = os.listdir(f"data/{gender}")
        for folder in folders:
            thread = threading.Thread(target=process_folder, args=(gender, folder, export_path, done))
            thread.start()
            threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Save the updated 'done' list to the JSON file
    with open("data/done.json", "w") as f:
        json.dump(done, f, indent=1)


if __name__ == "__main__":
    main()
