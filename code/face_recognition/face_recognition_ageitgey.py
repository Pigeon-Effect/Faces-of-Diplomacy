import os
import joblib
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import face_recognition
import face_recognition_models

# --- Fix: Set model directory for face recognition ---
models_path = os.path.join(os.path.dirname(face_recognition_models.__file__), 'models')
face_recognition_models.model_dir = models_path


def train_face_recognition_model(dataset_path, model_save_path):
    known_face_encodings = []
    known_face_names = []

    print("Starting dataset scan...")

    # Walk through directory structure
    for country_code in os.listdir(dataset_path):
        country_path = os.path.join(dataset_path, country_code)

        if not os.path.isdir(country_path):
            continue

        for politician_name in os.listdir(country_path):
            politician_path = os.path.join(country_path, politician_name)

            if not os.path.isdir(politician_path):
                continue

            print(f"Processing: {politician_path}")

            valid_images = 0
            for file in os.listdir(politician_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(politician_path, file)

                    try:
                        image = face_recognition.load_image_file(image_path)
                        face_encodings = face_recognition.face_encodings(image)

                        if len(face_encodings) == 1:
                            known_face_encodings.append(face_encodings[0])
                            known_face_names.append(politician_name)
                            valid_images += 1
                        else:
                            print(f" - Skipped {file}: {len(face_encodings)} faces detected")

                    except Exception as e:
                        print(f" - Error processing {file}: {str(e)}")
                        continue

            print(f" - Found {valid_images} valid images for {politician_name}")

    if not known_face_encodings:
        raise ValueError("No training data found. Check:\n"
                         "1. Dataset path is correct\n"
                         "2. Folders contain images\n"
                         "3. Face detection works on your images")

    # Encode labels
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(known_face_names)

    # Train classifier
    print("\nTraining classifier...")
    classifier = SVC(kernel='linear', probability=True)
    classifier.fit(known_face_encodings, encoded_labels)

    # Save model
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    joblib.dump({
        'classifier': classifier,
        'label_encoder': label_encoder,
        'classes': label_encoder.classes_
    }, model_save_path)

    print(f"\nTraining successful! Model saved to {model_save_path}")
    print(f"Total trained samples: {len(known_face_names)}")
    print(f"Unique politicians: {len(label_encoder.classes_)}")


# Configuration
dataset_path = r"C:\Users\Admin\Documents\Cultural Analytics\resources\wikimedia\filtered_cropped_augmented_100"
model_save_path = r"C:\Users\Admin\Documents\Cultural Analytics\models\politician_classifier.pkl"

# Start training
train_face_recognition_model(dataset_path, model_save_path)