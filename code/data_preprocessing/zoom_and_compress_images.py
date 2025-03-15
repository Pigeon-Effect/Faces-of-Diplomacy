import os
import face_recognition_models

models_path = os.path.join(os.path.dirname(face_recognition_models.__file__), 'models')
face_recognition_models.model_dir = models_path

import face_recognition
from PIL import Image


def process_images(input_root, output_root, crop_margin=0.25, target_size=(300, 300)):

    for root, dirs, files in os.walk(input_root):
        for file in files:
            if file.lower().endswith(('.jpg', '.png')):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_root)
                output_path = os.path.join(output_root, relative_path)
                output_dir = os.path.dirname(output_path)

                # Create output directory if it doesn't exist
                os.makedirs(output_dir, exist_ok=True)

                try:
                    # Load image and detect faces
                    image = face_recognition.load_image_file(input_path)
                    face_locations = face_recognition.face_locations(image)

                    if len(face_locations) == 1:
                        top, right, bottom, left = face_locations[0]

                        # Calculate crop margins
                        width = right - left
                        height = bottom - top
                        margin_width = int(width * crop_margin)
                        margin_height = int(height * crop_margin)

                        # Convert to PIL Image and crop
                        pil_image = Image.fromarray(image)
                        cropped_image = pil_image.crop((
                            max(0, left - margin_width),
                            max(0, top - margin_height),
                            min(pil_image.width, right + margin_width),
                            min(pil_image.height, bottom + margin_height)
                        ))

                        # Resize and save
                        cropped_image.resize(target_size).save(output_path)
                        print(f"Processed: {input_path} -> {output_path}")
                    else:
                        print(f"Skipped: {input_path} ({len(face_locations)} faces detected)")
                except Exception as e:
                    print(f"Error processing {input_path}: {str(e)}")


# Path configuration
input_root = "path_to_input_images"
output_root = "path_to_output_images"

# Start processing
process_images(input_root, output_root)
