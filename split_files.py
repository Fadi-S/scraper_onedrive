import os
import json
from distutils.dir_util import copy_tree

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
    servers[i % server_count]["male"].append(remaining_female[i])


from_path = "data"
to_path = "data/split"
os.makedirs(to_path, exist_ok=True)

for i in range(server_count):
    for path in servers[i]["male"]:
        copy_tree(os.path.join(from_path, "male", path), os.path.join(to_path, "male", path))

    for path in servers[i]["female"]:
        copy_tree(os.path.join(from_path, "female", path), os.path.join(to_path, "female", path))

