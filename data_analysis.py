"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Task 6 Data analysis: describes the raw landmark data from Task 5

@author: <B07> (100475742, 100174060, 100464504, 100481021)
@date:   27/11/2026
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("hand_landmarks.csv")

# dataset size and class distribution

print("Total rows:", len(df))
print("Images per letter:")
print(df["label"].value_counts().sort_index())

# where hands arent recognised
features = df.drop(columns="label")
zero_rows = (features == 0).all(axis=1)
print("Rows with no hand detected:", zero_rows.sum())
print("No-hand rows per letter:")
print(df[zero_rows]["label"].value_counts())

# duplicate rows
hand_rows = df[~zero_rows]
print("Duplicate rows (excluding no-hand):", hand_rows.duplicated().sum())
print("Duplicates per letter:")
print(hand_rows[hand_rows.duplicated()]["label"].value_counts())

# value ranges of the x,y,z coordinates
hand_features = hand_rows.drop(columns="label")
x_cols = hand_features.filter(like="x")
y_cols = hand_features.filter(like="y")
z_cols = hand_features.filter(like="z")
print("x range:", x_cols.min().min(), "to", x_cols.max().max())
print("y range:", y_cols.min().min(), "to", y_cols.max().max())
print("z range:", z_cols.min().min(), "to", z_cols.max().max())

# number of images per letter (1st plot)
counts = df["label"].value_counts().sort_index()
counts.plot(kind="bar")
plt.title("Number of images per letter")
plt.xlabel("Letter")
plt.ylabel("Count")
plt.savefig("class_distribution.png")
plt.show()

# spread of x,y,z coordinates (2nd plot)
plt.boxplot([x_cols.values.flatten(), y_cols.values.flatten(), z_cols.values.flatten()],tick_labels=["x", "y", "z"])
plt.title("Range of landmark coordinates")
plt.ylabel("Value")
plt.savefig("coordinate_ranges.png")
plt.show()