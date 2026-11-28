"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Task 6 Data preprocessing: cleans the raw landmark data from Task 5

@author: <B07> (100475742, 100174060, 100464504, 100481021)
@date:   28/11/2026
"""

import pandas as pd
import numpy as np

df = pd.read_csv("hand_landmarks.csv")
print("Rows before cleaning:", len(df))

# remove no-hand-detected rows
features = df.drop(columns="label")
zero_rows = (features == 0).all(axis=1)
df = df[~zero_rows]
print("Rows after removing no-hand rows:", len(df))

# remove duplicate rows found
df = df.drop_duplicates()
print("Rows after removing duplicates:", len(df))

# column names for the 21 landmarks
x_cols = [f"x{i}" for i in range(21)]
y_cols = [f"y{i}" for i in range(21)]
z_cols = [f"z{i}" for i in range(21)]
all_cols = x_cols + y_cols + z_cols

# normalise position so the wrist is at (0,0,0)
df[x_cols] = df[x_cols].sub(df["x0"], axis=0)
df[y_cols] = df[y_cols].sub(df["y0"], axis=0)
df[z_cols] = df[z_cols].sub(df["z0"], axis=0)

# normalise size
hand_size = np.sqrt(df["x9"]**2 + df["y9"]**2 + df["z9"]**2)
df[all_cols] = df[all_cols].div(hand_size, axis=0)

# outlier check: how far each hand is from its letter's average shape
average = df.groupby("label")[all_cols].transform("mean")
distance = np.sqrt(((df[all_cols] - average)**2).sum(axis=1))
print("Distance from letter average:")
print(distance.describe())

# encode labels: A=0, B=1, etc
letters = sorted(df["label"].unique())
label_map = {letter: number for number, letter in enumerate(letters)}
df["label_num"] = df["label"].map(label_map)
print("Label encoding:", label_map)

# save cleaned version for task 7
df.to_csv("cleaned_landmarks.csv", index=False)