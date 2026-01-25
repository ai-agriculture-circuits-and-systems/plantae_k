# PlantaeK Dataset

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue?logo=semver&logoColor=white)](https://github.com/your-repo/plantae_k)
[![GitHub stars](https://img.shields.io/github/stars/your-repo/plantae_k?style=flat&logo=github&label=Stars&color=orange&labelColor=orange&logoColor=white)](https://github.com/your-repo/plantae_k)
[![GitHub forks](https://img.shields.io/github/forks/your-repo/plantae_k?style=flat&logo=github&label=Forks&color=yellow&labelColor=yellow&logoColor=white)](https://github.com/your-repo/plantae_k)
[![GitHub watchers](https://img.shields.io/github/watchers/your-repo/plantae_k?style=flat&logo=github&label=Watchers&color=cyan&labelColor=cyan&logoColor=white)](https://github.com/your-repo/plantae_k)
[![GitHub issues](https://img.shields.io/github/issues/your-repo/plantae_k?style=flat&logo=github&label=Issues&color=red&labelColor=red&logoColor=white)](https://github.com/your-repo/plantae_k/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/your-repo/plantae_k?style=flat&logo=github&label=PRs&color=lime&labelColor=lime&logoColor=white)](https://github.com/your-repo/plantae_k/pulls)
[![GitHub contributors](https://img.shields.io/github/contributors/your-repo/plantae_k?style=flat&logo=github&label=Contributors&color=purple&labelColor=purple&logoColor=white)](https://github.com/your-repo/plantae_k/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/your-repo/plantae_k?style=flat&logo=github&label=Last%20Commit&color=gray&labelColor=gray&logoColor=white)](https://github.com/your-repo/plantae_k/commits)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.xxxxx-indigo?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.xxxxx)

A comprehensive dataset containing high-resolution images of plant leaves, divided into multiple categories based on species and health status. This dataset is particularly focused on native plants of Jammu and Kashmir. This dataset follows the standardized dataset structure specification.

- **Project page**: `https://data.mendeley.com/datasets/t6j2h22jpx/1`
- **Original paper**: (to be added)
- **Dataset repository**: `https://data.mendeley.com/datasets/t6j2h22jpx/1`
- **TensorFlow Dataset Catalog**: `https://www.tensorflow.org/datasets/catalog/plantae_k`

## TL;DR

- **Task**: Classification
- **Modality**: RGB
- **Platform**: Ground
- **Real/Synthetic**: Real
- **Images**: ~2,153 labeled images
- **Classes**: 8 plant species × 2 health statuses = 16 categories
  - **Apples**: healthy (160), diseased (191)
  - **Apricots**: healthy (86), diseased (184)
  - **Cherries**: healthy (117), diseased (95)
  - **Cranberries**: healthy (118), diseased (94)
  - **Grapes**: healthy (162), diseased (9)
  - **Peaches**: healthy (313), diseased (18)
  - **Pears**: healthy (114), diseased (114)
  - **Walnuts**: healthy (93), diseased (285)
- **Resolution**: Variable (high-resolution, e.g., 6000×4000 pixels)
- **Annotations**: COCO JSON (image-level via full-image boxes)
- **Total annotations**: ~2,153 (one per image for classification)
- **License**: CC BY 4.0 (see LICENSE)
- **Citation**: See below

## Table of Contents
- [Download](#download)
- [Dataset Structure](#dataset-structure)
- [Sample Images](#sample-images)
- [Annotation Schema](#annotation-schema)
- [Stats and Splits](#stats-and-splits)
- [Quick Start](#quick-start)
- [Evaluation and Baselines](#evaluation-and-baselines)
- [Datasheet (Data Card)](#datasheet-data-card)
- [Known Issues and Caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)

## Download

- **Original dataset**: `https://data.mendeley.com/datasets/t6j2h22jpx/1`
- **This repository**: Hosts structure and conversion scripts only; place the downloaded folders under this directory.
- **Local license file**: See `LICENSE` (CC BY 4.0).

## Dataset Structure

This dataset follows the standardized dataset structure specification:

```
plantae_k/
├── apples/
│   ├── diseased/
│   │   ├── csv/                      # CSV annotations per image
│   │   ├── json/                     # JSON annotations per image
│   │   ├── images/                   # Image files
│   │   └── sets/                     # Dataset splits (optional, category-level splits used)
│   ├── healthy/
│   │   ├── csv/
│   │   ├── json/
│   │   └── images/
│   ├── labelmap.json                # Label mapping (all subcategories)
│   └── sets/                         # Dataset splits (shared across subcategories)
│       ├── train.txt
│       ├── val.txt
│       ├── test.txt
│       ├── all.txt
│       └── train_val.txt
├── apricots/
│   └── ... (same structure as apples)
├── cherries/
│   └── ... (same structure as apples)
├── cranberries/
│   └── ... (same structure as apples)
├── grapes/
│   └── ... (same structure as apples)
├── peaches/
│   └── ... (same structure as apples)
├── pears/
│   └── ... (same structure as apples)
├── walnuts/
│   └── ... (same structure as apples)
├── annotations/                      # COCO format JSON (generated)
│   ├── apples_instances_train.json
│   ├── apples_instances_val.json
│   ├── apples_instances_test.json
│   └── ... (similar for other categories)
├── scripts/
│   ├── reorganize_dataset.py        # Reorganize dataset to standard structure
│   └── convert_to_coco.py           # Convert to COCO format
├── data/                             # Original data directory (preserved)
├── LICENSE
├── README.md
├── USAGE.md
└── requirements.txt
```

- Splits: `{category}/sets/train.txt`, `{category}/sets/val.txt`, `{category}/sets/test.txt` (and also `all.txt`, `train_val.txt`) list image basenames (no extension). Splits are shared across all subcategories within a category.

## Sample Images

Below are example images from this dataset. Paths are relative to this README location.

<table>
  <tr>
    <th>Category</th>
    <th>Sample</th>
  </tr>
  <tr>
    <td><strong>Apple - Healthy</strong></td>
    <td>
      <img src="apples/healthy/images/apple_h018.JPG" alt="Apple healthy example" width="260"/>
      <div align="center"><code>apples/healthy/images/apple_h018.JPG</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Apple - Diseased</strong></td>
    <td>
      <img src="apples/diseased/images/apple_d001.JPG" alt="Apple diseased example" width="260"/>
      <div align="center"><code>apples/diseased/images/apple_d001.JPG</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Apricot - Healthy</strong></td>
    <td>
      <img src="apricots/healthy/images/apricot_h001.JPG" alt="Apricot healthy example" width="260"/>
      <div align="center"><code>apricots/healthy/images/apricot_h001.JPG</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Cherry - Diseased</strong></td>
    <td>
      <img src="cherries/diseased/images/cherry_d001.JPG" alt="Cherry diseased example" width="260"/>
      <div align="center"><code>cherries/diseased/images/cherry_d001.JPG</code></div>
    </td>
  </tr>
</table>

## Annotation Schema

- **CSV per-image schema** (stored under `{category}/{subcategory}/csv/` folder):
  - Columns: `item, x, y, width, height, label`
  - For classification tasks, each image has a full-image bounding box: `[0, 0, image_width, image_height]`
  - The `label` field corresponds to the subcategory ID from `labelmap.json` (1=diseased, 2=healthy, etc.)
  - Example:
    ```csv
    #item,x,y,width,height,label
    0,0,0,6000,4000,1
    ```
  
- **JSON per-image format** (stored under `{category}/{subcategory}/json/`):

```json
{
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
  "images": [
    {
      "id": 9136804699,
      "width": 6000,
      "height": 4000,
      "file_name": "pear_d012.JPG",
      "size": 2314945,
      "format": "JPG",
      "url": "",
      "hash": "",
      "status": "success"
    }
  ],
  "annotations": [
    {
      "id": 9136804699,
      "image_id": 9136804699,
      "category_id": 1,
      "bbox": [0, 0, 6000, 4000],
      "area": 24000000,
      "iscrowd": 0
    }
  ],
  "categories": [
    {
      "id": 1,
      "name": "DISEASED",
      "supercategory": "PEAR"
    }
  ]
}
```

- **Label maps**: `{category}/labelmap.json` contains all subcategories for that category. Example (`apples/labelmap.json`):
```json
[
  {
    "object_id": 0,
    "label_id": 0,
    "keyboard_shortcut": "0",
    "object_name": "background"
  },
  {
    "object_id": 1,
    "label_id": 1,
    "keyboard_shortcut": "1",
    "object_name": "diseased"
  },
  {
    "object_id": 2,
    "label_id": 2,
    "keyboard_shortcut": "2",
    "object_name": "healthy"
  }
]
```

- **COCO-style** (generated via `scripts/convert_to_coco.py`):

```json
{
  "info": {
    "year": 2019,
    "version": "1.0.0",
    "description": "PlantaeK apples train split",
    "url": "https://data.mendeley.com/datasets/t6j2h22jpx/1"
  },
  "images": [
    {
      "id": 1,
      "file_name": "apples/healthy/images/apple_h018.JPG",
      "width": 6000,
      "height": 4000
    }
  ],
  "categories": [
    {
      "id": 1,
      "name": "diseased",
      "supercategory": "apples"
    },
    {
      "id": 2,
      "name": "healthy",
      "supercategory": "apples"
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1,
      "category_id": 2,
      "bbox": [0, 0, 6000, 4000],
      "area": 24000000,
      "iscrowd": 0
    }
  ]
}
```

## Stats and Splits

### Image Counts by Category

| Category | Diseased | Healthy | Total |
|----------|----------|---------|-------|
| Apples | 191 | 160 | 351 |
| Apricots | 184 | 86 | 270 |
| Cherries | 95 | 117 | 212 |
| Cranberries | 94 | 118 | 212 |
| Grapes | 9 | 162 | 171 |
| Peaches | 18 | 313 | 331 |
| Pears | 114 | 114 | 228 |
| Walnuts | 285 | 93 | 378 |
| **Total** | **990** | **1,163** | **~2,153** |

Note: Some images may be skipped due to file corruption or missing annotations.

### Dataset Splits

Splits are provided via `{category}/sets/*.txt`. You may define your own splits by editing those files.

Default split ratios:
- Training: 70%
- Validation: 15%
- Test: 15%

Splits are shared across all subcategories within each category (e.g., all healthy and diseased apples share the same train/val/test split).

## Quick Start

### Using COCO API

```python
from pycocotools.coco import COCO
import json

# Load COCO annotations
coco = COCO('annotations/apples_instances_train.json')

# Get all image IDs
img_ids = coco.getImgIds()
print(f"Total images: {len(img_ids)}")

# Get all category IDs
cat_ids = coco.getCatIds()
categories = [coco.loadCats([id])[0]['name'] for id in cat_ids]
print(f"Categories: {categories}")

# Load a specific image and its annotations
img_id = img_ids[0]
img_info = coco.loadImgs([img_id])[0]
ann_ids = coco.getAnnIds(imgIds=[img_id])
anns = coco.loadAnns(ann_ids)

print(f"Image: {img_info['file_name']}")
print(f"Size: {img_info['width']}x{img_info['height']}")
print(f"Annotations: {len(anns)}")
```

### Converting to COCO format

If you need to regenerate COCO annotations from CSV files:

```bash
python scripts/convert_to_coco.py --root . \
    --categories apples apricots cherries cranberries grapes peaches pears walnuts \
    --splits train val test
```

### Dependencies

**Required**:
- `Pillow>=9.5` (for image processing)

**Optional**:
- `pycocotools>=2.0.7` (for COCO API)

Install with:
```bash
pip install -r requirements.txt
```

## Evaluation and Baselines

- **Primary metric**: 
  - Classification: Accuracy, Precision, Recall, F1-score (per class and macro-averaged)
  - Per-class Accuracy: Accuracy for each health status (healthy vs. diseased)
  - Confusion Matrix: Per-class performance breakdown
- **Baseline results**: (to be added)

## Datasheet (Data Card)

### Motivation

This dataset was created to support research in plant disease detection and classification, particularly for native plants of the Jammu and Kashmir region, which is crucial for automated disease detection in agricultural applications.

### Composition

The dataset consists of:
- **Image types**: High-resolution photographs of plant leaves
- **Categories**: 8 plant species (apples, apricots, cherries, cranberries, grapes, peaches, pears, walnuts) with 2 health statuses each (healthy, diseased)
- **Annotation format**: Image-level classification annotations (via full-image bounding boxes)

### Collection Process

- **Source**: Dataset collected and curated by Vippon Preet Kour and Sakshi Arora, focusing on native plants of Jammu and Kashmir region
- **Annotation tool**: Images captured in field conditions using handheld devices
- **Validation**: Images organized by species and health status

### Preprocessing

- Images organized by species and health status
- Annotations provided in both JSON and CSV formats
- Full-image bounding boxes used for classification tasks
- Dataset reorganized to follow standardized structure specification

### Distribution

- Dataset is distributed under CC BY 4.0 license
- Original data available from Mendeley Data
- This repository provides standardized structure and conversion scripts

### Maintenance

- Dataset structure has been standardized according to the dataset structure specification
- COCO format annotations are generated from CSV files using the provided conversion script

## Known Issues and Caveats

1. **File Format**: Some image files may be corrupted or unreadable (particularly in grapes/healthy and peaches/healthy subcategories). These files are automatically skipped during conversion.

2. **Missing Annotations**: Some images may have empty JSON files. Empty CSV files are generated for these cases.

3. **Image Resolution**: Image resolutions vary significantly across the dataset (from small to very high resolution, e.g., 6000×4000 pixels).

4. **Coordinate System**: Bounding boxes use the standard COCO format: `[x, y, width, height]` where `(x, y)` is the top-left corner.

5. **Classification Task**: This dataset is designed for classification tasks. Each image has a full-image bounding box indicating the image-level category (healthy or diseased).

6. **Split Consistency**: Dataset splits are shared across all subcategories within each category to ensure consistent evaluation.

## License

This dataset is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

Check the original dataset terms and cite appropriately.

See `LICENSE` file for full license text.

## Citation

If you use this dataset in your research, please cite:

```bibtex
@misc{plantae_k_2019,
  author = {Vippon Preet Kour and Sakshi Arora},
  title = {PlantaeK: A leaf database of native plants of Jammu and Kashmir},
  howpublished = {Mendeley Data},
  year = {2019},
  url = {https://data.mendeley.com/datasets/t6j2h22jpx/1}
}
```

## Changelog

- **V1.0.0** (2025): Initial standardized structure and COCO conversion utility

## Contact

- **Maintainers**: Open to contributions via issue tracker
- **Original authors**: Vippon Preet Kour, Sakshi Arora
- **Source**: `https://data.mendeley.com/datasets/t6j2h22jpx/1`
