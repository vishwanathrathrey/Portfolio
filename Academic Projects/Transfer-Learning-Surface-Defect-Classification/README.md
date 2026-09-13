# Industrial Surface Defect Classification using Transfer Learning

## Overview

This project applies transfer learning to classify surface defects in steel images. It uses the NEU-DET dataset, a pretrained convolutional backbone, and a train/validation image-folder layout to build a practical industrial image-classification workflow.

## Recruiter Snapshot

This project demonstrates:
- **Computer Vision:** Building an image classification pipeline for real industrial defect detection.
- **Transfer Learning:** Reusing pretrained convolutional features instead of training from scratch.
- **Data Loading:** Working with directory-based image datasets and class-labelled folders.
- **Model Adaptation:** Fine-tuning a pretrained backbone with a lightweight classification head.
- **Validation Analysis:** Evaluating performance on a separate held-out validation split.

## Dataset

- **Dataset:** NEU Surface Defect Dataset
- **Classes:** `crazing`, `inclusion`, `patches`, `pitted`, `rolled-in_scale`, `scratches`
- **Training Images:** `data/NEU-DET/train/images/`
- **Validation Images:** `data/NEU-DET/validation/images/`
- **Annotations:** XML files in `data/NEU-DET/train/annotations/`

## Objectives

- Classify steel surface defects from grayscale industrial images.
- Use transfer learning to reduce training time and data requirements.
- Prepare a clean train/validation image workflow for reproducible experiments.
- Compare pretrained visual features against the target defect classes.
- Evaluate model behavior on the validation set.

## Project Workflow

1. **Dataset Understanding:** Inspect the class structure and annotation layout.
2. **Image Loading:** Load images from the training and validation folders.
3. **Preprocessing:** Prepare the data pipeline for model training.
4. **Model Setup:** Use a pretrained MobileNetV2-style architecture as the feature extractor.
5. **Fine-Tuning:** Train the classification head on the defect dataset.
6. **Validation:** Check how well the model generalizes to held-out images.

## Techniques Applied

| Technique | Application |
|---|---|
| **Transfer Learning** | Reusing pretrained feature extractors for an industrial vision task |
| **Image Classification** | Predicting surface defect categories from grayscale steel images |
| **Data Loading** | Directory-based image loading with class labels inferred from folders |
| **Model Fine-Tuning** | Training a lightweight classification head on top of pretrained features |
| **Validation Analysis** | Checking generalization on the held-out validation set |

## Results

- The notebook demonstrates a complete transfer-learning workflow for industrial surface defect classification.
- The dataset is organized in a way that works cleanly with folder-based image loading.
- The project uses a pretrained backbone to reduce the cost of training on a specialized dataset.
- Validation output in the notebook shows the model learning useful defect-class cues from the NEU-DET images.

## Key Insights

- Transfer learning is effective when labeled data is limited but the visual domain is still structured.
- The folder-based dataset layout makes class inference straightforward and reproducible.
- Industrial defect images benefit from a lighter fine-tuning strategy rather than full retraining.

## Key Learnings

- Pretrained vision models are a strong starting point for small, domain-specific datasets.
- Keeping train and validation folders explicit makes experiments easier to manage.
- A carefully prepared image pipeline matters as much as the network architecture.

## Future Work

- Try additional pretrained backbones for comparison.
- Add stronger image augmentation to improve robustness.
- Track class-wise metrics and confusion matrices more explicitly.
- Experiment with more advanced fine-tuning schedules.

## Repository Structure

```text
Transfer-Learning-Surface-Defect-Classification/
├── data/
│   └── NEU-DET/
├── Transfer_Learning_Surface_Defect.ipynb
└── README.md
```

## Notes

- The project follows the same top-level `data/` convention used by the other academic projects.
- The notebook should be executed from the project folder root so the relative image paths resolve correctly.