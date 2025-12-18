#!/usr/bin/env python3
"""
Reorganize PlantaeK dataset to standard structure.
Converts from: data/{SPECIES}/{HEALTH_STATUS}/
To: {category}/{subcategory}/{csv,json,images,sets}/
"""

import json
import shutil
import random
from pathlib import Path
from typing import Dict, List, Tuple

# Mapping from uppercase species names to lowercase plural category names
SPECIES_TO_CATEGORY = {
    "APPLE": "apples",
    "APRICOT": "apricots",
    "CHERRY": "cherries",
    "CRANBERRY": "cranberries",
    "GRAPES": "grapes",
    "PEACH": "peaches",
    "PEAR": "pears",
    "WALNUT": "walnuts",
}

# Mapping from uppercase health status to lowercase subcategory names
HEALTH_TO_SUBCATEGORY = {
    "DISEASED": "diseased",
    "HEALTHY": "healthy",
}

def create_directory_structure(root: Path, category: str, subcategory: str):
    """Create standard directory structure for a category/subcategory."""
    base_dir = root / category / subcategory
    for subdir in ["csv", "json", "images", "sets"]:
        (base_dir / subdir).mkdir(parents=True, exist_ok=True)
    return base_dir

def json_to_csv(json_path: Path, csv_path: Path):
    """Convert JSON annotation to CSV format (full image bounding box for classification)."""
    try:
        with json_path.open(encoding="utf-8") as f:
            data = json.load(f)
        
        if not data.get("annotations"):
            # No annotations, create empty CSV
            csv_path.write_text("#item,x,y,width,height,label\n", encoding="utf-8")
            return
        
        # Get the first annotation (should be full image bbox for classification)
        ann = data["annotations"][0]
        bbox = ann["bbox"]
        category_id = ann["category_id"]
        
        # Write CSV with header
        csv_content = "#item,x,y,width,height,label\n"
        csv_content += f"0,{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},{category_id}\n"
        csv_path.write_text(csv_content, encoding="utf-8")
    except Exception as e:
        print(f"Error converting {json_path} to CSV: {e}")
        # Create empty CSV on error
        csv_path.write_text("#item,x,y,width,height,label\n", encoding="utf-8")

def create_labelmap(root: Path, category: str, subcategories: List[str]):
    """Create labelmap.json for a category with all subcategories."""
    labelmap = [
        {
            "object_id": 0,
            "label_id": 0,
            "keyboard_shortcut": "0",
            "object_name": "background"
        }
    ]
    
    for idx, subcat in enumerate(sorted(subcategories), start=1):
        labelmap.append({
            "object_id": idx,
            "label_id": idx,
            "keyboard_shortcut": str(idx),
            "object_name": subcat
        })
    
    labelmap_path = root / category / "labelmap.json"
    with labelmap_path.open("w", encoding="utf-8") as f:
        json.dump(labelmap, f, indent=2, ensure_ascii=False)
    
    return labelmap

def create_splits(root: Path, category: str, subcategory: str, image_stems: List[str], 
                  train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """Create train/val/test split files."""
    # Shuffle for random split
    random.seed(42)  # For reproducibility
    shuffled = sorted(image_stems)
    random.shuffle(shuffled)
    
    total = len(shuffled)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    train_stems = shuffled[:train_end]
    val_stems = shuffled[train_end:val_end]
    test_stems = shuffled[val_end:]
    
    sets_dir = root / category / subcategory / "sets"
    sets_dir.mkdir(parents=True, exist_ok=True)
    
    # Write split files
    (sets_dir / "train.txt").write_text("\n".join(train_stems) + "\n", encoding="utf-8")
    (sets_dir / "val.txt").write_text("\n".join(val_stems) + "\n", encoding="utf-8")
    (sets_dir / "test.txt").write_text("\n".join(test_stems) + "\n", encoding="utf-8")
    (sets_dir / "all.txt").write_text("\n".join(sorted(image_stems)) + "\n", encoding="utf-8")
    (sets_dir / "train_val.txt").write_text("\n".join(train_stems + val_stems) + "\n", encoding="utf-8")
    
    return len(train_stems), len(val_stems), len(test_stems)

def reorganize_dataset(data_dir: Path, output_dir: Path):
    """Main function to reorganize the dataset."""
    data_dir = Path(data_dir)
    output_dir = Path(output_dir)
    
    # Collect all categories and subcategories
    category_subcategories = {}
    all_images = {}  # (category, subcategory) -> list of (image_path, json_path, stem)
    
    # First pass: collect all files
    for species_dir in sorted(data_dir.iterdir()):
        if not species_dir.is_dir():
            continue
        
        species_name = species_dir.name
        if species_name not in SPECIES_TO_CATEGORY:
            print(f"Warning: Unknown species {species_name}, skipping")
            continue
        
        category = SPECIES_TO_CATEGORY[species_name]
        
        for health_dir in sorted(species_dir.iterdir()):
            if not health_dir.is_dir():
                continue
            
            health_name = health_dir.name
            if health_name not in HEALTH_TO_SUBCATEGORY:
                print(f"Warning: Unknown health status {health_name}, skipping")
                continue
            
            subcategory = HEALTH_TO_SUBCATEGORY[health_name]
            
            if category not in category_subcategories:
                category_subcategories[category] = []
            if subcategory not in category_subcategories[category]:
                category_subcategories[category].append(subcategory)
            
            # Find all images and their corresponding JSON files
            key = (category, subcategory)
            if key not in all_images:
                all_images[key] = []
            
            for file_path in sorted(health_dir.iterdir()):
                if file_path.suffix.upper() in [".JPG", ".JPEG", ".PNG", ".jpg", ".png"]:
                    stem = file_path.stem
                    json_path = health_dir / f"{stem}.json"
                    if not json_path.exists():
                        json_path = health_dir / f"{stem}.JSON"
                    
                    all_images[key].append((file_path, json_path, stem))
    
    # Second pass: reorganize files
    print("Reorganizing dataset structure...")
    for (category, subcategory), image_list in all_images.items():
        print(f"Processing {category}/{subcategory}: {len(image_list)} images")
        
        # Create directory structure
        base_dir = create_directory_structure(output_dir, category, subcategory)
        
        # Move files and create CSV
        image_stems = []
        for image_path, json_path, stem in image_list:
            # Move image
            dest_image = base_dir / "images" / image_path.name
            shutil.copy2(image_path, dest_image)
            
            # Move JSON
            if json_path.exists():
                dest_json = base_dir / "json" / json_path.name
                shutil.copy2(json_path, dest_json)
                
                # Create CSV from JSON
                csv_path = base_dir / "csv" / f"{stem}.csv"
                json_to_csv(json_path, csv_path)
            else:
                print(f"Warning: JSON file not found for {image_path}")
            
            image_stems.append(stem)
        
        # Create splits (using category-level splits, shared across subcategories)
        # We'll create splits at category level later
        pass
    
    # Create labelmaps and category-level splits
    print("\nCreating labelmaps and splits...")
    for category, subcategories in category_subcategories.items():
        # Create labelmap
        labelmap = create_labelmap(output_dir, category, subcategories)
        print(f"Created labelmap for {category} with {len(subcategories)} subcategories")
        
        # Collect all image stems for this category (across all subcategories)
        all_category_stems = []
        for subcategory in subcategories:
            key = (category, subcategory)
            if key in all_images:
                all_category_stems.extend([stem for _, _, stem in all_images[key]])
        
        # Create category-level splits (shared across subcategories)
        sets_dir = output_dir / category / "sets"
        sets_dir.mkdir(parents=True, exist_ok=True)
        
        random.seed(42)
        shuffled = sorted(set(all_category_stems))
        random.shuffle(shuffled)
        
        total = len(shuffled)
        train_end = int(total * 0.7)
        val_end = train_end + int(total * 0.15)
        
        train_stems = shuffled[:train_end]
        val_stems = shuffled[train_end:val_end]
        test_stems = shuffled[val_end:]
        
        (sets_dir / "train.txt").write_text("\n".join(train_stems) + "\n", encoding="utf-8")
        (sets_dir / "val.txt").write_text("\n".join(val_stems) + "\n", encoding="utf-8")
        (sets_dir / "test.txt").write_text("\n".join(test_stems) + "\n", encoding="utf-8")
        (sets_dir / "all.txt").write_text("\n".join(sorted(set(all_category_stems))) + "\n", encoding="utf-8")
        (sets_dir / "train_val.txt").write_text("\n".join(train_stems + val_stems) + "\n", encoding="utf-8")
        
        print(f"Created splits for {category}: train={len(train_stems)}, val={len(val_stems)}, test={len(test_stems)}")
    
    print("\nReorganization complete!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Reorganize PlantaeK dataset to standard structure")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data",
        help="Input data directory (default: <script_dir>/../data)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Output directory (default: <script_dir>/..)",
    )
    
    args = parser.parse_args()
    reorganize_dataset(args.data_dir, args.output_dir)
