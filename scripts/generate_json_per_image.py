import os
import json
import random
import time
from PIL import Image

# Generate a unique 10-digit id: 7 random digits + 3-digit timestamp

def generate_unique_id(existing_ids):
    while True:
        rand_part = random.randint(1000000, 9999999)
        time_part = int(time.time()) % 1000  # 3-digit timestamp
        unique_id = int(f"{rand_part}{time_part:03d}")
        if unique_id not in existing_ids:
            existing_ids.add(unique_id)
            return unique_id

def process_image(image_path, category_id, category_name, supercategory_name, existing_ids, with_annotation=True):
    with Image.open(image_path) as img:
        width, height = img.size
    image_id = generate_unique_id(existing_ids)
    image_info = {
        "id": image_id,
        "width": width,
        "height": height,
        "file_name": os.path.basename(image_path),
        "size": os.path.getsize(image_path),
        "format": os.path.splitext(image_path)[-1][1:].upper(),
        "url": "",
        "hash": "",
        "status": "success"
    }
    if with_annotation:
        annotation = {
            "id": image_id,
            "image_id": image_id,
            "category_id": category_id,
            "bbox": [0, 0, width, height],
            "area": width * height,
            "iscrowd": 0
        }
        annotations = [annotation]
    else:
        annotations = []
    categories = [
        {"id": category_id, "name": category_name, "supercategory": supercategory_name}
    ]
    data = {
        "info": {
            "description": "data",
            "version": "1.0",
            "year": 2025,
            "contributor": "search engine",
            "source": "augmented",
            "license": {
                "name": "Creative Commons Attribution 4.0 International",
                "url": "https://creativecommons.org/licenses/by/4.0/"
            }
        },
        "images": [image_info],
        "annotations": annotations,
        "categories": categories
    }
    json_path = os.path.splitext(image_path)[0] + ".json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def build_category_id_map(data_dir):
    category_id_map = {}
    current_id = 1
    for fruit_name in os.listdir(data_dir):
        fruit_dir = os.path.join(data_dir, fruit_name)
        if not os.path.isdir(fruit_dir):
            continue
        for category_name in os.listdir(fruit_dir):
            category_dir = os.path.join(fruit_dir, category_name)
            if not os.path.isdir(category_dir):
                continue
            key = (fruit_name, category_name)
            if key not in category_id_map:
                category_id_map[key] = current_id
                current_id += 1
    return category_id_map

def main():
    existing_ids = set()
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    category_id_map = build_category_id_map(data_dir)
    for fruit_name in os.listdir(data_dir):
        fruit_dir = os.path.join(data_dir, fruit_name)
        if not os.path.isdir(fruit_dir):
            continue
        for category_name in os.listdir(fruit_dir):
            category_dir = os.path.join(fruit_dir, category_name)
            if not os.path.isdir(category_dir):
                continue
            category_id = category_id_map[(fruit_name, category_name)]
            for fname in os.listdir(category_dir):
                if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                    fpath = os.path.join(category_dir, fname)
                    process_image(
                        fpath,
                        category_id,
                        category_name,
                        fruit_name,
                        existing_ids,
                        with_annotation=True
                    )

if __name__ == "__main__":
    main() 