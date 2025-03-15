import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from torchvision.transforms import functional as F
import random


def augment_image(image_path, output_path):
    img = Image.open(image_path).convert('RGB')

    for _ in range(3):  # Try up to 3 times for valid augmentation
        try:
            # Geometric transformations
            if random.random() > 0.5:
                img = F.hflip(img)

            angle = random.uniform(-10, 10)
            img = F.rotate(img, angle, expand=False)

            # Scaling and translation
            scale = random.uniform(0.9, 1.1)
            dx = random.randint(-15, 15)
            dy = random.randint(-15, 15)
            img = F.affine(img, angle=0, translate=(dx, dy), scale=scale, shear=0)

            # Color adjustments
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(random.uniform(0.7, 1.3))

            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(random.uniform(0.7, 1.3))

            gamma = random.uniform(0.7, 1.3)
            img = F.adjust_gamma(img, gamma)

            # Add Gaussian noise
            if random.random() > 0.5:
                arr = np.array(img).astype(np.float32)
                noise = np.random.normal(0, random.uniform(1, 5), arr.shape)
                arr = arr + noise
                arr = np.clip(arr, 0, 255).astype(np.uint8)
                img = Image.fromarray(arr)

            # Synthetic occlusions
            if random.random() > 0.7:
                draw = img.copy()
                occl_size = random.randint(30, 70)
                x = random.randint(50, 250 - occl_size)
                y = random.randint(50, 250 - occl_size)

                if random.random() > 0.5:
                    draw.paste((0, 0, 0), (x, y, x + occl_size, y + occl_size))
                else:
                    crop = draw.crop((x, y, x + occl_size, y + occl_size))
                    crop = crop.filter(ImageFilter.GaussianBlur(radius=5))
                    draw.paste(crop, (x, y, x + occl_size, y + occl_size))

                img = Image.blend(img, draw, random.uniform(0.3, 0.7))

            img = img.resize((300, 300))
            img.save(output_path)
            return True

        except Exception as e:
            print(f"Augmentation failed, retrying: {str(e)}")
            continue

    return False


def process_politician_folders(root_dir, target_count=100):
    for country_folder in os.listdir(root_dir):
        country_path = os.path.join(root_dir, country_folder)

        if not os.path.isdir(country_path):
            continue

        for politician_folder in os.listdir(country_path):
            politician_path = os.path.join(country_path, politician_folder)

            if not os.path.isdir(politician_path):
                continue

            # Process this politician's folder
            image_files = []
            for f in os.listdir(politician_path):
                if f.lower().endswith(('.jpg', '.png')):
                    image_files.append(f)

            current_count = len(image_files)
            if current_count == 0:
                print(f"Skipping empty folder: {politician_path}")
                continue

            if current_count >= target_count:
                continue

            needed = target_count - current_count
            print(f"Processing {politician_path} - needs {needed} more images")

            for i in range(needed):
                success = False
                while not success:
                    # Pick random source image
                    src_file = random.choice(image_files)
                    base, ext = os.path.splitext(src_file)
                    output_file = f"{base}_aug_{i}{ext}"
                    output_path = os.path.join(politician_path, output_file)

                    # Ensure unique filename
                    while os.path.exists(output_path):
                        i += 1
                        output_file = f"{base}_aug_{i}{ext}"
                        output_path = os.path.join(politician_path, output_file)

                    # Attempt augmentation
                    success = augment_image(os.path.join(politician_path, src_file), output_path)


# Configuration
root_directory = "path_to_china_daily_dataset"
process_politician_folders(root_directory)
