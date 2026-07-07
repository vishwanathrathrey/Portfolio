# Identifying Key Entities in Recipe Data: A CRF-based NER Approach

## Overview

This project implements a **Named Entity Recognition (NER)** pipeline using **Conditional Random Fields (CRF)** to extract structured information from unstructured recipe ingredient lists. The system identifies and classifies tokens into three entity categories: **ingredients**, **quantities**, and **units**. This enables the transformation of free-text recipe data into structured, queryable information suitable for recipe management systems, dietary tracking applications, and e-commerce platforms.

The workflow demonstrates a complete natural language processing (NLP) pipeline including data ingestion, validation, exploratory analysis, feature engineering, class weighting, model training, evaluation, and error analysis.

## Dataset

- **Source**: `ingredient_and_quantity.json`
- **Format**: JSON with two columns:
  - `input`: Raw ingredient list text (space-separated tokens)
  - `pos`: Corresponding NER labels (quantity, ingredient, unit)
- **Original Size**: 285 recipes, 2 columns
- **After Cleaning**: 280 recipes with valid token-label alignment
- **Training/Validation Split**: 70/30 stratified split
  - Training: 196 recipes, 7,114 tokens
  - Validation: 84 recipes, 2,876 tokens
- **Note**: Only sample data is included in this repository. The full dataset is excluded due to size constraints.

## Objectives

- Develop a CRF-based NER model for entity extraction from recipe texts
- Perform comprehensive exploratory data analysis on ingredient and unit distributions
- Engineer domain-specific features that capture lexical, syntactic, and contextual patterns
- Implement class weighting to address data imbalance
- Evaluate model performance across all entity classes
- Conduct error analysis to identify systematic weaknesses
- Save the trained model for future inference and deployment

## Project Workflow

### 1. Data Collection
- Loaded JSON dataset into pandas DataFrame
- Verified data structure and completeness

### 2. Data Cleaning
- Tokenized input and POS strings into token lists
- Identified and removed 5 invalid rows with token-label length mismatches
- Validated consistent token-label alignment across all rows

### 3. Exploratory Data Analysis (EDA)
- Analyzed token distributions and label frequencies
- Identified most frequent ingredients and units
- Visualized top entities using bar charts
- Compared training and validation distributions to ensure consistent patterns

### 4. Train-Validation Split
- Split dataset using 70/30 ratio with random seed 42 for reproducibility
- Confirmed unique labels: ingredient, quantity, unit

### 5. Feature Engineering
- Designed comprehensive feature extraction function (`word2features`)
- Implemented core features (lexical, morphological, syntactic)
- Created domain-specific quantity and unit detection features
- Added contextual features (previous/next token information)
- Built keyword sets for unit and quantity detection
- Computed inverse frequency class weights with ingredient penalty

### 6. Model Development
- Initialized CRF model with LBFGS optimization
- Configured regularization parameters (L1=0.5, L2=1.0)
- Trained model with class-weighted features
- Saved model using joblib for future use

### 7. Model Evaluation
- Evaluated training performance using classification report and confusion matrix
- Evaluated validation performance using classification report and confusion matrix
- Compared training vs. validation metrics
- Performed detailed error analysis on validation predictions

### 8. Error Analysis
- Flattened validation predictions and true labels
- Identified 197 misclassified tokens (6.85% error rate)
- Analyzed errors by label type with class weights
- Examined contextual patterns in misclassifications
- Generated actionable recommendations for improvement

## Techniques and Concepts Applied

| Technique | Application |
|-----------|-------------|
| **Conditional Random Fields** | Sequence labeling for token classification |
| **Feature Engineering** | Lexical, syntactic, morphological, and contextual features |
| **Class Weighting** | Inverse frequency method to address data imbalance |
| **LBFGS Optimization** | Quasi-Newton optimizer for CRF training |
| **L1/L2 Regularization** | Feature sparsity and overfitting prevention |
| **Tokenization** | Splitting raw strings into token sequences |
| **spaCy Integration** | Extracting POS tags, lemmas, dependency relations |
| **Regex Pattern Matching** | Quantity detection (fractions, decimals, numbers) |
| **Confusion Matrix Analysis** | Error pattern identification by class |
| **Error Analysis** | Systematic investigation of misclassification patterns |

## Models Used

### Conditional Random Fields (CRF)

**Rationale**: CRF is a probabilistic framework for sequence labeling that models the conditional probability of label sequences given observation sequences. It was selected because:

- It captures contextual dependencies between labels
- It avoids the label bias problem found in HMMs
- It allows incorporation of complex overlapping features
- It scales well to sequence labeling tasks

**Hyperparameters**:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `algorithm` | 'lbfgs' | Quasi-Newton optimization for efficient convergence |
| `c1` | 0.5 | L1 regularization for feature sparsity |
| `c2` | 1.0 | L2 regularization to prevent overfitting |
| `max_iterations` | 100 | Sufficient iterations for convergence |
| `all_possible_transitions` | True | Complete state transition modeling |

## Results

### Training Performance

| Label | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| ingredient | 0.96 | 0.98 | 0.97 |
| quantity | 0.93 | 0.88 | 0.91 |
| unit | 0.94 | 0.86 | 0.89 |
| **Overall Accuracy** | | | **0.95** |

### Validation Performance

| Label | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| ingredient | 0.94 | 0.97 | 0.96 |
| quantity | 0.92 | 0.86 | 0.89 |
| unit | 0.89 | 0.78 | 0.83 |
| **Overall Accuracy** | | | **0.93** |

### Key Observations

- The model generalizes well with only a 2% drop in accuracy from training to validation
- Ingredient recognition shows the strongest performance (97% accuracy on validation)
- Unit classification is most challenging (78% accuracy on validation)
- Higher class weights for quantity and unit did not translate to higher accuracy
- Ingredient class achieved high accuracy despite having the lowest class weight (0.22)

### Error Distribution

| Label | Class Weight | Accuracy | Total Samples | Errors |
|-------|--------------|----------|---------------|--------|
| ingredient | 0.2227 | 97.06% | 2,107 | 62 |
| quantity | 2.4197 | 86.13% | 411 | 57 |
| unit | 2.9240 | 78.21% | 358 | 78 |
| **Total** | | | **2,876** | **197** |

## Key Insights

### Data Quality Insights
- **Token-label mismatch detection** was critical: 5 invalid rows (1.75% of data) had inconsistent token-count alignments, confirming the need for thorough validation before modeling.

### Frequency Analysis Insights
- The most frequent ingredient was "powder" (129 occurrences), followed by "Salt" (102), "seeds" (89), and "Green" (85)
- The most frequent unit was "teaspoon" (162), followed by "cup" (136), "tablespoon" (99), and "grams" (63)
- The presence of both singular and plural forms of units highlights the importance of keyword set comprehensiveness

### Class Performance Insights
- **Ingredient recognition** (97% accuracy) is highly effective due to high frequency and distinctive contextual patterns
- **Quantity detection** (86% accuracy) faces challenges when fractions are separated from their units by cooking terms
- **Unit classification** (78% accuracy) is the most challenging due to inherent ambiguity between unit terms and ingredient names (e.g., "seeds" as part of "cumin seeds")

### Class Weight Impact
- Higher class weights for unit (2.92) and quantity (2.42) did not overcome the inherent difficulty of these classes
- This suggests that class imbalance is not the primary issue; instead, more sophisticated feature engineering is needed for units

### Contextual Error Patterns
- **Unit → Ingredient**: Common units like "teaspoon", "tablespoon", "cloves", "cup" are misclassified as ingredients when appearing in ambiguous contexts
- **Ingredient → Unit**: Words like "seeds", "powder", "chillies" are misclassified as units when they appear near numeric tokens
- **Quantity → Ingredient**: Fractions and numbers (1/2, 2, 3, 1/4) are misclassified as ingredients when separated from their units
- Cooking terms (finely, chopped, grated) frequently disrupt quantity-unit adjacency patterns

### Business Implications
- Automated extraction of structured ingredient data enables searchable recipe databases, nutritional analysis, automated grocery lists, and e-commerce integration
- High ingredient accuracy suggests immediate practical utility for database creation

## Key Learnings

### 1. Feature Engineering is Critical for Sequence Labeling
- The success of the CRF model depended heavily on comprehensive feature design
- Combining lexical features (token, lemma), syntactic features (POS, dependency), morphological features (shape, capitalization), and contextual features (neighboring tokens) proved essential
- Domain-specific features (quantity/unit detection) were crucial for performance

### 2. Class Imbalance and Weighting
- The ingredient class dominated training data (74.8% of tokens), leading to potential bias
- Inverse frequency weighting with penalty for the majority class helped balance learning
- However, class weights alone couldn't resolve the difficulty of unit classification

### 3. Contextual Ambiguity is the Main Challenge
- Unit classification challenges are primarily due to contextual ambiguity rather than data imbalance
- Words like "seeds" can be a unit when following a number but an ingredient when part of a compound name
- The same token can appear in different contexts with different labels, requiring robust contextual understanding

### 4. Data Quality Validation
- Input-POS length mismatch detection is a simple but critical quality check
- 1.75% of the original data had inconsistencies, which could have degraded model performance if not addressed

### 5. Model Generalization
- With only 2% drop in overall accuracy from training (95%) to validation (93%), the model shows strong generalization
- Minimal overfitting indicates appropriate regularization and model complexity

## Repository Structure

Recipe-NER-CRF/
├── data/
│ └── sample/
│ └── ingredient_and_quantity_sample.json
├── notebook.ipynb
├── report.pdf
└── README.md


## Notes

- Full dataset is excluded from this repository due to size constraints
- Sample data is provided for reproducibility and testing
- The notebook can be run with the full dataset for complete results
- This project was completed as part of my **MSc in Machine Learning and Artificial Intelligence**

## Future Work

- Incorporate contextual embeddings (BERT, RoBERTa) for ambiguous term resolution
- Implement hybrid CRF-BiLSTM architecture for improved sequence modeling
- Expand training data with more diverse recipe formats and cuisines
- Develop post-processing rules enforcing quantity → unit → ingredient sequence patterns
- Add support for additional entity types (cooking methods, temperatures, equipment)
- Implement active learning for challenging edge cases

## References

1. Lafferty, J., McCallum, A., and Pereira, F. (2001). Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data. *Proceedings of ICML*.

2. Sutton, C., and McCallum, A. (2012). An Introduction to Conditional Random Fields. *Foundations and Trends in Machine Learning*, 4(4), 267-373.

3. Scikit-learn CRFsuite documentation: https://sklearn-crfsuite.readthedocs.io/

4. spaCy documentation for linguistic features: https://spacy.io/api/annotation

5. Bird, S., Klein, E., and Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media.