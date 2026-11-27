"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes hand landmark feature extraction using MediaPipe for Task 5

@author: <B07> (100475742, 100174060, 100464504, 100481021)
@date:   26/11/2026
"""

import csv
from pathlib import Path
import mediapipe as mp

IMAGE_FOLDER = Path("Images")
MODEL_FILE = "hand_landmarker.task"
OUTPUT_FILE = "hand_landmarks.csv"


def extract_features(landmarker, image_path):
    """Get 21 x/y/z points, or return 63 zeros when no hand is found."""
    image = mp.Image.create_from_file(str(image_path))
    result = landmarker.detect(image)
    if not result.hand_landmarks:
        return [0.0] * 63

    features = []
    for point in result.hand_landmarks[0]:
        features.extend([point.x, point.y, point.z])
    return features


def main():
    if not IMAGE_FOLDER.is_dir():
        raise FileNotFoundError(f"Missing image folder: {IMAGE_FOLDER}")
    if not Path(MODEL_FILE).is_file():
        raise FileNotFoundError(f"Missing MediaPipe model: {MODEL_FILE}")

    columns = []
    for number in range(21):
        columns.extend([f"x{number}", f"y{number}", f"z{number}"])

    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=MODEL_FILE),
        running_mode=mp.tasks.vision.RunningMode.IMAGE,
        num_hands=1,
    )

    total = 0
    no_hand = 0
    with mp.tasks.vision.HandLandmarker.create_from_options(options) as landmarker, \
         open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(columns + ["label"])

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            folder = IMAGE_FOLDER / letter
            if not folder.is_dir():
                print(f"Missing letter folder: {folder}")
                continue

            for image_path in sorted(folder.iterdir()):
                if not image_path.is_file() or image_path.suffix.lower() != ".jpg":
                    continue

                features = extract_features(landmarker, image_path)
                writer.writerow(features + [letter])
                total += 1
                if features == [0.0] * 63:
                    no_hand += 1
                    print(f"No hand detected: {image_path}")

    print(f"Processed {total} photos; {no_hand} had no detected hand")
    print(f"Saved dataset: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()