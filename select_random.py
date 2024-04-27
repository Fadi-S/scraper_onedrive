import random
import os
import pandas as pd
import shutil
from tqdm import tqdm

# Load index.csv
index = pd.read_csv('data/index.csv')


# Separate female and male samples
female = index[index['gender'] == 'female']
male = index[index['gender'] == 'male']

male = male.sample(frac=1).reset_index(drop=True)

male = male.iloc[:len(female)]

stacked_samples = pd.concat([female, male], axis=0)

# Create folder for random samples
os.makedirs('data/random_samples', exist_ok=True)
stacked_samples.to_csv('data/random_samples.csv', index=False, columns=index.columns)
print(stacked_samples.columns)

# Copy files to random_samples folder
for filename in tqdm(stacked_samples['file_name']):
    shutil.copy(f'data/audios/{filename}', f'data/random_samples/{filename}')

print("Random samples copied to 'data/random_samples' folder.")
