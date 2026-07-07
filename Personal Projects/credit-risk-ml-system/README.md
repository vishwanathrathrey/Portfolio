# Credit Risk ML System

An end-to-end local machine learning application for predicting credit risk using the Home Credit Default Risk dataset. This project demonstrates a full-stack approach to building and deploying a machine learning model on a local machine.

## Overview

This is a local end-to-end ML application that combines:
- **Data Processing**: A PySpark-based pipeline for cleaning and transforming data.
- **Model Training**: A Scikit-learn pipeline for training a credit risk prediction model.
- **API Serving**: A FastAPI backend to serve the trained model for real-time predictions.
- **Frontend Visualization**: A React-based dashboard for user interaction and displaying results.

## Features

- **Credit Risk Prediction**: Predicts the likelihood of a loan applicant defaulting.
- **PySpark Preprocessing**: Utilizes PySpark for efficient data cleaning, feature transformation, and feature engineering.
- **Scikit-learn Model Training**: Implements a machine learning pipeline with Scikit-learn for model training and evaluation.
- **FastAPI Inference API**: Provides a robust REST API for model inference, health checks, and metrics.
- **React Dashboard**: A user-friendly interface built with React and Vite for entering applicant data and viewing predictions.
- **Docker-Based Local Setup**: Containerized services using Docker and Docker Compose for easy local deployment.
- **Model Metrics and Health Monitoring**: Endpoints to monitor the application's health and model performance.

## Architecture

A simple workflow diagram of the system:

```
Dataset
   ↓
PySpark Data Processing
   ↓
Feature Engineering
   ↓
Scikit-learn Model Training
   ↓
Joblib Saved Model
   ↓
FastAPI Backend
   ↓
React Dashboard
   ↓
Credit Risk Prediction
```

## Project Structure

```
Credit-Risk-ML-System/
├── api/
├── ml/
├── pyspark/
├── frontend/
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js and npm
- Docker and Docker Compose

### Environment Setup
1.  Clone the repository.
2.  Create and activate a Python virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running Locally

#### 1. Train the Model
Run the training script to process data and save the model:
```powershell
python ml/train_model.py
```

#### 2. Run Backend API (FastAPI)
```powershell
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

#### 3. Run Frontend Dashboard (React)
```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

### Running with Docker
This is the recommended way to run the entire application.
```powershell
docker-compose up
```
The frontend will be available at `http://localhost:5173` and the backend at `http://localhost:8000`.

## API Documentation

The API is served by FastAPI and includes the following endpoints:

#### `GET /health`
Checks the health of the API.
- **Response (200 OK)**:
  ```json
  {
    "status": "ok"
  }
  ```

#### `GET /metrics`
Provides model metrics (this is a placeholder and can be expanded).
- **Response (200 OK)**:
  ```json
  {
    "model_metrics": {
      "auc": 0.75
    }
  }
  ```

#### `POST /predict`
Accepts applicant data and returns a credit risk prediction.
- **Request Body**:
  ```json
  {
    "SK_ID_CURR": 100002,
    "AMT_INCOME_TOTAL": 202500.0,
    "AMT_CREDIT": 406597.5,
    "AMT_ANNUITY": 24700.5,
    "AMT_GOODS_PRICE": 351000.0
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "prediction": 1,
    "probability": 0.85
  }
  ```

## Machine Learning Pipeline

The ML pipeline consists of the following stages:
1.  **Preprocessing**: Raw data from the Home Credit Default Risk dataset is cleaned and prepared using a PySpark pipeline (`pyspark/data_processor.py`).
2.  **Feature Engineering**: New features are created from existing ones to improve model performance.
3.  **Training**: A Scikit-learn pipeline is used to train a classification model (e.g., Logistic Regression, LightGBM) on the processed data (`ml/train_model.py`).
4.  **Evaluation**: The model is evaluated using metrics like AUC.
5.  **Serialization**: The trained model pipeline is serialized using Joblib and saved locally.
6.  **Inference**: The FastAPI backend loads the serialized model to make real-time predictions. The API aligns incoming request fields with the feature set the model was trained on.

## Key Learnings

- **End-to-End ML Pipeline Development**: Building a complete machine learning system from data processing to deployment.
- **FastAPI for Model Serving**: Creating efficient, production-ready APIs for machine learning models.
- **Frontend-Backend Integration**: Connecting a React frontend with a Python backend for a seamless user experience.
- **Advanced Data Preprocessing**: Using PySpark for handling large datasets and complex transformations.
- **Docker for Reproducibility**: Containerizing a multi-service application for consistent local deployment.

## Future Enhancements

- **Model Explainability**: Integrate SHAP or LIME to explain model predictions.
- **Advanced Feature Engineering**: Explore more sophisticated feature engineering techniques.
- **Model Monitoring**: Implement a system to monitor model performance and data drift over time.
- **Authentication**: Add user authentication to the frontend and backend.
- **Cloud Deployment**: Adapt the application for deployment on a cloud platform (e.g., AWS, GCP, Azure).
- **CI/CD Integration**: Set up a CI/CD pipeline for automated testing and deployment.
- **Automated Retraining**: Create a workflow for automatically retraining the model on new data.

## About

This is a personal project by an AI/ML Engineer to demonstrate skills in building and deploying full-stack machine learning applications.