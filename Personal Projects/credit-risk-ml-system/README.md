# End-to-End Credit Risk ML System

## Overview

This project implements a complete, end-to-end machine learning system for credit risk assessment. The system is built using a modern MLOps stack, including Docker for containerization, PySpark for distributed data processing, MLflow for experiment tracking, and a Flask API for model serving. It features a full CI/CD pipeline for automated training, evaluation, and deployment, along with a Streamlit-based frontend for interactive predictions.

## Recruiter Snapshot

This project demonstrates:
- **End-to-End MLOps Pipeline:** Proficiency in designing and implementing a complete MLOps workflow, from data ingestion and distributed processing (PySpark) to automated model training, versioning (MLflow), containerization (Docker), and API deployment (Flask).
- **Distributed Data Processing:** Expertise in using Apache PySpark to build a scalable, fault-tolerant data processing pipeline capable of handling large-scale financial datasets.
- **CI/CD for Machine Learning:** Skill in creating a CI/CD pipeline that automates model training, evaluation, and deployment, ensuring reproducibility and rapid iteration.
- **Microservices Architecture:** Competency in building a system based on a microservices architecture, with distinct services for data processing, model training, and API serving, all orchestrated with Docker Compose.
- **Full-Stack ML Application:** Ability to build and integrate all components of a machine learning application, including a data backend, a machine learning model, a serving API, and an interactive user-facing frontend (Streamlit).

## Features

- **Distributed Data Pipeline:** A robust data pipeline built with PySpark for scalable data ingestion, cleaning, and feature engineering.
- **Automated Model Training:** A training pipeline that automatically trains a credit risk model (e.g., Logistic Regression, Gradient Boosting) and logs experiments with MLflow.
- **Model Serving API:** A RESTful API built with Flask to serve the trained model and provide real-time credit risk predictions.
- **Interactive Frontend:** A user-friendly web interface built with Streamlit that allows users to input applicant data and receive instant credit risk assessments.
- **Containerized Environment:** The entire system is containerized using Docker and orchestrated with Docker Compose for easy setup and deployment.
- **CI/CD Automation:** A fully automated CI/CD pipeline for continuous training and deployment of the model.

## Architecture

The system is designed as a collection of containerized microservices that work together to deliver the credit risk assessment service.

1.  **Data Ingestion & Processing (PySpark):**
    - A PySpark job runs on a schedule or trigger to ingest raw data from a source (e.g., HDFS, S3, local files).
    - It performs data cleaning, validation, feature engineering, and prepares the data for model training.
    - The processed data is stored in a feature store or data warehouse.

2.  **Model Training & Tracking (MLflow):**
    - A training script fetches the latest data and trains a machine learning model.
    - MLflow is used to track experiments, log model parameters, metrics, and artifacts.
    - The best-performing model is registered in the MLflow Model Registry.

3.  **Model Serving (Flask API):**
    - A Flask-based web server loads the latest production model from the MLflow Model Registry.
    - It exposes a `/predict` endpoint that accepts applicant data in JSON format.
    - It returns a credit risk prediction (e.g., "Low Risk," "High Risk") and a probability score.

4.  **Frontend (Streamlit):**
    - A Streamlit application provides a simple web form for users to enter applicant details.
    - It sends a request to the Flask API and displays the returned prediction to the user.

5.  **Orchestration (Docker Compose):**
    - Docker Compose is used to define and run the multi-container application, including the PySpark cluster, MLflow server, Flask API, and Streamlit frontend.

## Project Workflow

1.  Raw credit data is ingested by the PySpark pipeline.
2.  The data is cleaned, transformed, and engineered into features suitable for modeling.
3.  The automated training pipeline runs, using the new data to train and evaluate several models.
4.  The best model is versioned and promoted to "Production" in the MLflow Model Registry.
5.  The Flask API automatically loads the new production model.
6.  A user accesses the Streamlit frontend, enters applicant information, and clicks "Predict."
7.  The frontend sends the data to the Flask API.
8.  The API returns a prediction, which is displayed to the user.

## Techniques and Concepts Applied

| Technique | Application |
|---|---|
| **Distributed Computing** | Using PySpark for scalable and resilient data processing. |
| **MLOps** | Implementing a full MLOps lifecycle with experiment tracking (MLflow) and CI/CD. |
| **Containerization** | Using Docker to create reproducible environments for each service. |
| **Microservices** | Designing the system as a set of independent, containerized services. |
| **Model Serving** | Deploying a machine learning model as a REST API using Flask. |
| **Interactive UI** | Building a user-friendly frontend with Streamlit for model interaction. |
| **CI/CD for ML** | Automating the model training and deployment process. |

## Key Learnings

- **The Importance of a Data Pipeline:** A robust and automated data pipeline is the foundation of any reliable ML system. Using PySpark ensured that the system could scale with growing data volumes.
- **MLflow for Reproducibility:** MLflow was crucial for tracking experiments and managing the model lifecycle, making the entire process transparent and reproducible.
- **Docker for Consistency:** Containerizing each component of the system eliminated "it works on my machine" problems and ensured a consistent environment from development to production.
- **Separation of Concerns:** The microservices architecture allowed for a clear separation of concerns, making the system easier to develop, test, and maintain.

## Future Work

- **Advanced Model Monitoring:** Implement a dedicated monitoring service to track model drift, data drift, and prediction performance over time.
- **Cloud Deployment:** Deploy the entire system to a cloud platform like AWS or GCP using Kubernetes for orchestration.
- **A/B Testing:** Enhance the API to support A/B testing of different model versions in production.
- **Feature Store Integration:** Integrate with a dedicated feature store (e.g., Feast) for more robust feature management.

## Repository Structure

```
Credit-Risk-ML-System/
├── api/                    # Flask API for model serving
├── data/                   # Sample data
├── frontend/               # Streamlit frontend application
├── hadoop/                 # Docker setup for Hadoop/Spark cluster
├── ml/                     # Model training and MLflow tracking code
├── models/                 # Saved model artifacts
├── pyspark/                # PySpark data processing jobs
├── docker-compose.yml      # Docker Compose orchestration file
├── Dockerfile              # Dockerfile for the main application
└── requirements.txt        # Python dependencies
```

## Notes
- This project is a comprehensive demonstration of building a production-grade machine learning system, showcasing skills across data engineering, MLOps, and software development.
