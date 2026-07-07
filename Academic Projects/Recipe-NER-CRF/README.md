# Identifying Key Entities in Recipe Data: A CRF-based NER Approach

## Overview

This project implements a **Named Entity Recognition (NER)** pipeline using **Conditional Random Fields (CRF)** to extract structured information from unstructured recipe ingredient lists. The system identifies and classifies tokens into three key entity categories: **ingredients**, **quantities**, and **units**. This enables the transformation of free-text recipe data into a structured, queryable format suitable for recipe management systems, dietary tracking applications, and e-commerce platforms.

## Recruiter Snapshot

This project demonstrates:
- **Natural Language Processing (NLP):** Proficiency in building a complete NLP pipeline for a sequence labeling task (NER), a core competency in modern AI.
- **Advanced Feature Engineering for Text:** Skill in designing and implementing a rich set of lexical, syntactic, and contextual features tailored for text data, which is critical for the performance of classical NLP models.
- **Classical NLP Models (CRF):** Experience with Conditional Random Fields, a foundational statistical model for structured prediction tasks like NER, showcasing an understanding of non-deep-learning NLP techniques.
- **Information Extraction:** Ability to build a system that extracts structured data (entities) from unstructured text, a fundamental task in enterprise AI for document processing, knowledge base creation, and data enrichment.
- **Model Evaluation and Error Analysis:** Competency in evaluating sequence models using appropriate metrics (precision, recall, F1-score) and performing detailed error analysis to identify model weaknesses and guide improvements.

## Dataset

- **Source**: A JSON file containing recipe ingredient strings and their corresponding labels.
- **Labels**: `ingredient`, `quantity`, `unit`.
- **Size**: 280 cleaned recipes, split into training (196) and validation (84) sets.
- **Note**: Only sample data is included in this repository.

## Objectives

- Develop a CRF-based NER model to extract entities from recipe texts.
- Engineer domain-specific features that capture lexical, syntactic, and contextual patterns.
- Implement class weighting to address the natural imbalance in the data.
- Evaluate model performance across all entity classes and conduct a thorough error analysis.
- Save the trained model for future inference and deployment.

## Project Workflow

1.  **Data Cleaning and Preparation:**
    - Loaded and validated the JSON dataset, removing rows with token-label mismatches.
    - Split the data into training (70%) and validation (30%) sets.
2.  **Feature Engineering:**
    - Designed a comprehensive feature extraction function (`word2features`) that captures:
        - **Lexical & Morphological Features:** Word identity, suffix, shape, capitalization.
        - **Syntactic Features:** POS tags and dependency relations from spaCy.
        - **Contextual Features:** Features of neighboring tokens to provide a context window.
        - **Domain-Specific Features:** Custom logic to detect quantities (e.g., "1/2", "2.5") and units (e.g., "cup", "grams").
3.  **Model Development:**
    - Implemented class weighting using an inverse frequency approach to handle the imbalanced distribution of labels.
    - Initialized and trained a CRF model using LBFGS optimization and L1/L2 regularization.
4.  **Evaluation and Error Analysis:**
    - Evaluated the model on both training and validation sets using precision, recall, and F1-score.
    - Performed a detailed error analysis on the validation set to identify common misclassification patterns (e.g., "unit" -> "ingredient").

## Techniques and Concepts Applied

| Technique | Application |
|---|---|
| **Conditional Random Fields (CRF)** | A powerful statistical model for sequence labeling and structured prediction. |
| **Feature Engineering** | Creating a rich set of lexical, syntactic, morphological, and contextual features for text. |
| **Class Weighting** | Using an inverse frequency method to address data imbalance and improve model fairness. |
| **spaCy Integration** | Leveraging spaCy for advanced linguistic features like POS tags, lemmas, and dependency relations. |
| **Error Analysis** | Systematically investigating misclassifications to understand model weaknesses and guide future improvements. |

## Results

| Set | Accuracy | Ingredient F1 | Quantity F1 | Unit F1 |
|---|---|---|---|---|
| **Training** | 95% | 0.97 | 0.91 | 0.89 |
| **Validation** | 93% | 0.96 | 0.89 | 0.83 |

- The model demonstrates strong generalization with only a 2% drop in accuracy from training to validation.
- **Ingredient** recognition is highly effective (96% F1-score), making the model immediately useful for practical applications.
- **Unit** classification is the most challenging task (83% F1-score), primarily due to contextual ambiguity where a word can be both a unit and an ingredient (e.g., "cloves").

## Key Learnings

- **Feature Engineering is Crucial:** The success of the CRF model was heavily dependent on the comprehensive, domain-specific feature set. This highlights the importance of feature engineering in classical NLP.
- **Context is Key for Ambiguity:** The main challenge in this task is contextual ambiguity, not class imbalance. Words like "seeds" or "cloves" require strong contextual features to be correctly classified.
- **Error Analysis Drives Improvement:** The detailed error analysis provided clear, actionable insights, such as the need for more robust features to differentiate between units and ingredients in ambiguous contexts.

## Future Work

- **Hybrid Deep Learning Model:** Implement a hybrid Bi-LSTM-CRF architecture to leverage deep learning for automatic feature extraction while retaining the CRF's strength in sequence modeling.
- **Pre-trained Embeddings:** Incorporate contextual embeddings (e.g., BERT) to better handle ambiguous terms and improve overall performance.
- **Expand Training Data:** Augment the dataset with more diverse recipe formats to improve the model's robustness and generalization.

## Repository Structure

```
Recipe-NER-CRF/
├── Notebook.ipynb      # Jupyter Notebook with all code and analysis
├── README.md           # This file
└── data/
    └── sample/         # Directory for sample data
```

## Notes
- This project was completed as part of my **MSc in Machine Learning and Artificial Intelligence**, showcasing my ability to build a sophisticated NLP pipeline for information extraction.
