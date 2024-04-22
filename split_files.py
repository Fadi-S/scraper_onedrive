import json
import os
import shutil


def copytree(src, dst):
    if os.path.isfile(src):
        shutil.copy2(src, dst)
    else:
        files = os.listdir(src)
        os.makedirs(dst, exist_ok=True)
        for file in files:
            copytree(os.path.join(src, file), os.path.join(dst, file).__str__())


done = json.load(open("data/done.json"))
all_male = os.listdir("data/male")
all_female = os.listdir("data/female")

remaining_male = []
remaining_female = []

for folder in all_male:
    if folder in done:
        continue

    remaining_male.append(folder)

for folder in all_female:
    if folder in done:
        continue

    remaining_female.append(folder)


servers = [
    {"male": [], "female": []},
    {"male": [], "female": []},
    {"male": [], "female": []},
    {"male": [], "female": []},
]
server_count = len(servers)

for i in range(len(remaining_male)):
    servers[i % server_count]["male"].append(remaining_male[i])

for i in range(len(remaining_female)):
    servers[i % server_count]["female"].append(remaining_female[i])


from_path = "data"
to_path = "data/split"
os.makedirs(to_path, exist_ok=True)

for i in range(server_count):
    for path in servers[i]["male"]:
        dest = os.path.join(to_path, str(i + 1), "male", path)
        os.makedirs(dest, exist_ok=True)
        copytree(os.path.join(from_path, "male", path), dest)

    for path in servers[i]["female"]:
        dest = os.path.join(to_path, str(i + 1), "female", path)
        os.makedirs(dest, exist_ok=True)
        copytree(os.path.join(from_path, "female", path), dest)

