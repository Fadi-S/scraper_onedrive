import random
import os
import pandas as pd

# Load index.csv
index = pd.read_csv('data/index.csv')

# Select 60,000 random samples
random_samples = random.sample(range(len(index)), 70_000)

# Save random samples to a new csv file
index.iloc[random_samples].to_csv('data/random_samples.csv', index=False)

# Save random samples to a new folder
os.makedirs('data/random_samples', exist_ok=True)
for i in random_samples:
    os.system(f'cp data/audios/{index.iloc[i, 0]} data/random_samples/{index.iloc[i, 0]}')