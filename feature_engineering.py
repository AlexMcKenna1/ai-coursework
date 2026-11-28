"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Task 6 adds distance features to the cleaned landmark data

@author: <B07> (100475742, 100174060, 100464504, 100481021)
@date:   27/11/2026
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_landmarks.csv")

tips = {"thumb": 4, "index": 8, "middle": 12, "ring": 16, "pinky": 20}

# distance from the thumb tip to each other fingertip
for name, point in tips.items():
    if name == "thumb":
        continue
    df[f"thumb_{name}_dist"] = np.sqrt(
        (df[f"x{point}"] - df["x4"])**2 +
        (df[f"y{point}"] - df["y4"])**2 +
        (df[f"z{point}"] - df["z4"])**2
    )

# distance from the wrist to each fingertip
for name, point in tips.items():
    df[f"wrist_{name}_dist"] = np.sqrt(
        df[f"x{point}"]**2 +
        df[f"y{point}"]**2 +
        df[f"z{point}"]**2
    )

print("New distance features:")
print(df.filter(like="_dist").describe())

# trains a random forest and rank which features it relied on
feature_cols = [c for c in df.columns if c not in ["label", "label_num"]]
X = df[feature_cols]
y = df["label"]

forest = RandomForestClassifier(random_state=42)
forest.fit(X, y)

importance = pd.Series(forest.feature_importances_, index=feature_cols)
importance = importance.sort_values(ascending=False)
print("Top 15 most important features:")
print(importance.head(15))

# top 15 features by importance (plot)
importance.head(15).plot(kind="bar")
plt.title("Top 15 most important features")
plt.xlabel("Feature")
plt.ylabel("Importance")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()

# save dataset for task 7
df.to_csv("features.csv", index=False)