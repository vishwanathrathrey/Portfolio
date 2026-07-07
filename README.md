# Machine Learning, Data Engineering, and Generative AI Portfolio

Welcome to my portfolio. This repository showcases my journey and project work as I transition from a traditional Software Engineering background into the fields of Machine Learning, Data Engineering, and Generative AI.

## About This Repository

This collection includes a mix of academic coursework and personal projects.

*   **Academic Projects**: These demonstrate my foundational understanding of core machine learning concepts, including Exploratory Data Analysis (EDA), data cleaning, feature engineering, model building, and evaluation.
*   **Personal Projects**: These are practical, hands-on implementations showcasing my skills in building end-to-end systems, including data engineering pipelines, API development, MLOps principles, and Generative AI applications.

### Key Concepts & Technologies

| Category              | Skills & Concepts                                                                                             |
| --------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Machine Learning**  | EDA, Data Cleaning, Feature Engineering, Feature Selection, Data Visualization, Classification, Regression, Model Evaluation, Hyperparameter Tuning |
| **Data Engineering**  | ETL Pipelines, API Development, Docker, Data Modeling                                                         |
| **Generative AI**     | LLM Integration, Prompt Engineering, AI-driven Code Analysis                                                  |
| **Software & MLOps**  | FastAPI, Git, CI/CD, Model Deployment, System Design                                                          |

---

## Projects

The projects are organized into two categories. For detailed information about each project, please see the `README.md` file inside its folder.

### Personal Projects

These projects were built to solve practical problems and demonstrate my ability to design, build, and deploy data-driven applications.

| Project                 | Description                                                                                                                            |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **[AI Code Review](./Personal%20Projects/AI%20Code%20Review)**      | An automated code review system that uses a Large Language Model (LLM) to analyze pull requests, identify issues, and post comments.      |
| **[Credit Risk ML System](./Personal%20Projects/credit-risk-ml-system)** | An end-to-end machine learning system that predicts credit risk. Includes a data pipeline, model training, and a REST API for predictions. |
| **[Customer Data Pipeline](./Personal%20Projects/customer-data-pipeline)**| A data engineering project to build a robust ETL pipeline for processing customer data from multiple sources into a data warehouse.      |

### Academic Projects

These projects were completed as part of my MSc coursework. They demonstrate my understanding of fundamental ML concepts and data analysis techniques.

| Project                    | Description                                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------- |
| **[Car Price Prediction](./Academic%20Projects/Car%20Price)**   | A regression project to predict the price of used cars based on their features.                         |
| **[CardioRisk Prediction](./Academic%20Projects/CardioRisk)**  | A classification project to predict the risk of cardiovascular disease based on patient health data.    |
| **[File Handling](./Academic%20Projects/File%20Handling)** | Examples of file handling operations in Python. |
| **[Flight Data Analysis](./Academic%20Projects/Flight%20Mini%20assignmrnt)**   | An exploratory data analysis (EDA) of flight data to uncover patterns and insights.                     |
| **[Lung Cancer Analysis](./Academic%20Projects/Lung%20Cancer%20Mini%20Assignment)**   | An analysis of lung cancer patient data to identify key risk factors.                                   |
| **[NYC Taxi Analysis](./Academic%20Projects/NYC%20Taxi%20Analysis)**      | An EDA of the NYC taxi dataset to analyze trip patterns and fare structures.                            |
| **[Traffic Data Analysis](./Academic%20Projects/Traffic%20Data%20Analysis)**  | An ETL and data analysis project on traffic data to understand congestion patterns.                     |

---

## Learning Progression

My skills have progressed from foundational data analysis to building complex, end-to-end AI systems. This path reflects a continuous effort to deepen my expertise and apply it to practical, real-world scenarios.

1.  **Data Analysis & Visualization**: Began with analyzing datasets to extract insights and visualize patterns.
2.  **Feature Engineering & Machine Learning**: Moved on to building and evaluating predictive models.
3.  **Data Engineering & API Development**: Advanced to creating robust data pipelines and deploying models via APIs.
4.  **MLOps Concepts**: Gained experience with containerization (Docker) and system design for ML.
5.  **Generative AI**: Currently focused on leveraging Large Language Models to build intelligent applications.

Thank you for visiting my portfolio. I am actively seeking opportunities where I can apply my skills to solve challenging problems in AI and Data Engineering.


2. Start the API and frontend locally:

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

3. Train the model if needed:

```bash
python ml/train_model.py
```

### AI Code Review

1. Move to the project folder:

```bash
cd "AI Code Review"
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the webhook server:

```bash
python webhook_server.py
```

## Data Notes

- This repository includes sample datasets for learning and demonstration.
- Full production datasets are not included.
- The credit risk project uses the Home Credit Default Risk dataset from Kaggle and stores its data notes in `credit-risk-ml-system/data/README.md`.
