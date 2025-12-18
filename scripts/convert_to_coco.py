#!/usr/bin/env python3
"""
Convert PlantaeK dataset annotations to COCO JSON format.
Supports multi-class classification with subcategories (healthy/diseased).
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image

def read_split_list(split_file: Path) -> List[str]:
    """Read image base names (without extension) from a split file."""
    if not split_file.exists():
        return []
    lines = [line.strip() for line in split_file.read_text(encoding="utf-8").splitlines()]
    return [line for line in lines if line]

def image_size(image_path: Path) -> Tuple[int, int]:
    """Return (width, height) for an image path using PIL."""
    try:
        with Image.open(image_path) as img:
            return img.width, img.height
    except Exception as e:
        print(f"Warning: Cannot read image {image_path}: {e}")
        return 0, 0

def parse_csv_boxes(csv_path: Path) -> List[Dict]:
    """Parse a single CSV file and return bounding boxes with category IDs."""
    if not csv_path.exists():
        return []
    
    boxes = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                x = float(row.get('x', 0))
                y = float(row.get('y', 0))
                width = float(row.get('width', 0))
                height = float(row.get('height', 0))
                label = int(row.get('label', 1))
                
                if width > 0 and height > 0:
                    boxes.append({
                        'bbox': [x, y, width, height],
                        'area': width * height,
                        'category_id': label
                    })
            except (ValueError, KeyError):
                continue
    
    return boxes

def load_labelmap(labelmap_path: Path) -> Dict[str, int]:
    """Load labelmap.json and return a mapping from subcategory name to category_id."""
    if not labelmap_path.exists():
        return {}
    
    with labelmap_path.open(encoding="utf-8") as f:
        labelmap = json.load(f)
    
    # Create mapping: subcategory name -> category_id
    mapping = {}
    for item in labelmap:
        if item.get("object_id", 0) > 0:  # Skip background
            mapping[item["object_name"]] = item["object_id"]
    
    return mapping

def collect_annotations_for_split(
    category_root: Path,
    split: str,
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """Collect COCO dictionaries for images, annotations, and categories.
    Supports structure: {category}/{subcategory}/ subdirectories.
    """
    sets_dir = category_root / "sets"
    split_file = sets_dir / f"{split}.txt"
    image_stems = set(read_split_list(split_file))
    
    # Load labelmap
    labelmap_path = category_root / "labelmap.json"
    subcategory_to_id = load_labelmap(labelmap_path)
    
    if not image_stems:
        # Fall back to all images if no split file
        image_stems = set()
        for subcategory_dir in category_root.iterdir():
            if subcategory_dir.is_dir() and subcategory_dir.name not in ["sets"]:
                images_dir = subcategory_dir / "images"
                if images_dir.exists():
                    image_stems.update({p.stem for p in images_dir.glob("*.png")})
                    image_stems.update({p.stem for p in images_dir.glob("*.jpg")})
                    image_stems.update({p.stem for p in images_dir.glob("*.JPG")})
                    image_stems.update({p.stem for p in images_dir.glob("*.jpeg")})
                    image_stems.update({p.stem for p in images_dir.glob("*.JPEG")})
    
    images: List[Dict] = []
    anns: List[Dict] = []
    
    # Build categories from labelmap
    categories: List[Dict] = []
    if labelmap_path.exists():
        with labelmap_path.open(encoding="utf-8") as f:
            labelmap = json.load(f)
        for item in labelmap:
            if item.get("object_id", 0) > 0:  # Skip background
                categories.append({
                    "id": item["object_id"],
                    "name": item["object_name"],
                    "supercategory": category_root.name
                })
    else:
        # Fallback: try to infer from subdirectories
        subcategories = []
        for subcategory_dir in category_root.iterdir():
            if subcategory_dir.is_dir() and subcategory_dir.name not in ["sets"]:
                subcategories.append(subcategory_dir.name)
        for idx, subcat in enumerate(sorted(subcategories), start=1):
            categories.append({
                "id": idx,
                "name": subcat,
                "supercategory": category_root.name
            })
            subcategory_to_id[subcat] = idx
    
    image_id_counter = 1
    ann_id_counter = 1
    
    # Find all subcategory directories
    subcategory_dirs = []
    for subcategory_dir in category_root.iterdir():
        if subcategory_dir.is_dir() and subcategory_dir.name not in ["sets"]:
            subcategory_dirs.append(subcategory_dir)
    
    for stem in sorted(image_stems):
        # Try each subcategory directory
        img_path = None
        subcategory = None
        csv_path = None
        
        for subcat_dir in subcategory_dirs:
            images_dir = subcat_dir / "images"
            for ext in ['.png', '.jpg', '.JPG', '.PNG', '.jpeg', '.JPEG']:
                test_path = images_dir / f"{stem}{ext}"
                if test_path.exists():
                    img_path = test_path
                    subcategory = subcat_dir.name
                    csv_path = subcat_dir / "csv" / f"{stem}.csv"
                    break
            if img_path:
                break
        
        if not img_path:
            continue
        
        width, height = image_size(img_path)
        if width == 0 or height == 0:
            print(f"Warning: Skipping invalid image {img_path}")
            continue
        
        images.append({
            "id": image_id_counter,
            "file_name": f"{category_root.name}/{subcategory}/images/{img_path.name}",
            "width": width,
            "height": height,
        })
        
        if csv_path and csv_path.exists():
            for box in parse_csv_boxes(csv_path):
                # Map subcategory name to category_id if needed
                category_id = box['category_id']
                if subcategory in subcategory_to_id:
                    category_id = subcategory_to_id[subcategory]
                
                anns.append({
                    "id": ann_id_counter,
                    "image_id": image_id_counter,
                    "category_id": category_id,
                    "bbox": box['bbox'],
                    "area": box['area'],
                    "iscrowd": 0,
                })
                ann_id_counter += 1
        
        image_id_counter += 1
    
    return images, anns, categories

def build_coco_dict(
    images: List[Dict],
    anns: List[Dict],
    categories: List[Dict],
    description: str,
) -> Dict:
    """Build a complete COCO dict from components."""
    return {
        "info": {
            "year": 2019,
            "version": "1.0.0",
            "description": description,
            "url": "https://data.mendeley.com/datasets/t6j2h22jpx/1",
        },
        "images": images,
        "annotations": anns,
        "categories": categories,
        "licenses": [],
    }

def convert(
    root: Path,
    out_dir: Path,
    categories: List[str],
    splits: List[str],
    combined: bool = False,
) -> None:
    """Convert selected categories and splits to COCO JSON files."""
    out_dir.mkdir(parents=True, exist_ok=True)
    
    all_images = []
    all_anns = []
    all_categories = []
    category_id_offset = 1
    
    for category in categories:
        category_root = root / category
        
        if not category_root.exists():
            print(f"Warning: Category directory {category_root} does not exist, skipping")
            continue
        
        for split in splits:
            images, anns, categories_list = collect_annotations_for_split(
                category_root, split
            )
            
            if combined:
                # Adjust category IDs for combined file
                category_id_map = {}
                for cat in categories_list:
                    old_id = cat["id"]
                    new_id = category_id_offset
                    category_id_map[old_id] = new_id
                    cat["id"] = new_id
                    all_categories.append(cat)
                    category_id_offset += 1
                
                # Adjust annotation category IDs
                for ann in anns:
                    if ann["category_id"] in category_id_map:
                        ann["category_id"] = category_id_map[ann["category_id"]]
                
                all_images.extend(images)
                all_anns.extend(anns)
            else:
                desc = f"PlantaeK {category} {split} split"
                coco = build_coco_dict(images, anns, categories_list, desc)
                out_path = out_dir / f"{category}_instances_{split}.json"
                out_path.write_text(json.dumps(coco, indent=2), encoding="utf-8")
                print(f"Generated: {out_path} ({len(images)} images, {len(anns)} annotations)")
    
    if combined:
        for split in splits:
            # Filter images and annotations for this split
            split_images = []
            split_anns = []
            split_image_ids = set()
            
            for category in categories:
                category_root = root / category
                sets_dir = category_root / "sets"
                split_file = sets_dir / f"{split}.txt"
                image_stems = set(read_split_list(split_file))
                
                # Find images for this split
                for img in all_images:
                    if any(stem in img["file_name"] for stem in image_stems):
                        if img["id"] not in split_image_ids:
                            split_images.append(img)
                            split_image_ids.add(img["id"])
            
            # Find annotations for split images
            split_image_id_set = {img["id"] for img in split_images}
            for ann in all_anns:
                if ann["image_id"] in split_image_id_set:
                    split_anns.append(ann)
            
            desc = f"PlantaeK combined {split} split"
            coco = build_coco_dict(split_images, split_anns, all_categories, desc)
            out_path = out_dir / f"combined_instances_{split}.json"
            out_path.write_text(json.dumps(coco, indent=2), encoding="utf-8")
            print(f"Generated: {out_path} ({len(split_images)} images, {len(split_anns)} annotations)")

def main():
    parser = argparse.ArgumentParser(description="Convert PlantaeK annotations to COCO JSON")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Dataset root directory",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory for COCO JSON files (default: <root>/annotations)",
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        default=None,
        help="Category names to convert (default: all categories found)",
    )
    parser.add_argument(
        "--splits",
        nargs="+",
        default=["train", "val", "test"],
        choices=["train", "val", "test"],
        help="Dataset splits to generate (default: train val test)",
    )
    parser.add_argument(
        "--combined",
        action="store_true",
        help="Generate combined COCO JSON files for all categories",
    )
    
    args = parser.parse_args()
    
    if args.out is None:
        args.out = args.root / "annotations"
    
    # Find all categories if not specified
    if args.categories is None:
        args.categories = []
        for item in args.root.iterdir():
            if item.is_dir() and (item / "labelmap.json").exists():
                args.categories.append(item.name)
        args.categories = sorted(args.categories)
    
    if not args.categories:
        print("Error: No categories found. Please specify --categories or ensure labelmap.json files exist.")
        sys.exit(1)
    
    convert(
        root=args.root,
        out_dir=args.out,
        categories=args.categories,
        splits=args.splits,
        combined=args.combined,
    )

if __name__ == "__main__":
    main()
