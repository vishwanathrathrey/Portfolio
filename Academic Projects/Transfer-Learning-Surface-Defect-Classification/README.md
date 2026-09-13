# Industrial Surface Defect Classification using Transfer Learning

## Overview

This project applies transfer learning to classify surface defects in steel images. The notebook uses the NEU-DET dataset under a top-level `data/` folder, a pretrained convolutional backbone, and a train/validation image-folder layout to build a practical defect-classification workflow.

## Dataset

- **Dataset:** NEU Surface Defect Dataset
- **Classes:** `crazing`, `inclusion`, `patches`, `pitted`, `rolled-in_scale`, `scratches`
- **Training Images:** `data/NEU-DET/train/images/`
- **Validation Images:** `data/NEU-DET/validation/images/`
- **Annotations:** XML files in `data/NEU-DET/train/annotations/`

## What the notebook covers

1. Inspect the dataset structure and label distribution.
2. Load images from the training and validation folders.
3. Prepare the image pipeline for transfer learning.
4. Fine-tune a pretrained CNN, using MobileNetV2 as the reference architecture.
5. Evaluate model performance on the validation split.

## Techniques and Concepts

| Technique | Application |
|---|---|
| **Transfer Learning** | Reusing pretrained feature extractors for an industrial vision task |
| **Image Classification** | Predicting surface defect categories from grayscale steel images |
| **Data Loading** | Directory-based image loading with class labels inferred from folders |
| **Model Fine-Tuning** | Training a lightweight classification head on top of pretrained features |
| **Validation Analysis** | Checking generalization on the held-out validation set |

## Repository Structure

```text
Transfer-Learning-Surface-Defect-Classification/
├── data/
│   └── NEU-DET/
├── Transfer_Learning_Surface_Defect_Vishwanath_R_Athrey.ipynb
└── README.md
```

## Notes

- The project now follows the same top-level `data/` convention used by the other academic projects.
- The notebook expects to be executed from the project folder root so the relative image paths resolve correctly.