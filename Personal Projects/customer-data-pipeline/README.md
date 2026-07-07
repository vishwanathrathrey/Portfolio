# Customer Data Pipeline

A containerized, end-to-end data pipeline that ingests customer data from a mock API, processes it, and stores it in a PostgreSQL database. This project demonstrates a microservices architecture using Flask, FastAPI, and Docker.

## Overview

This project implements a complete data pipeline within a local, containerized environment. It showcases the integration of multiple services to create a robust system for data ingestion and retrieval. The pipeline consists of three core services orchestrated with Docker Compose:

1.  **Mock Data Server (Flask)**: A RESTful API that serves paginated customer data in JSON format, simulating a real-world data source.
2.  **Pipeline Service (FastAPI)**: The central component that ingests data from the mock server, validates it, and stores it in the PostgreSQL database. It also provides its own API to query the processed data.
3.  **PostgreSQL Database**: A persistent relational database for storing customer records.

## Features

- **Microservices Architecture**: Decoupled services for data generation, processing, and storage.
- **Containerized Deployment**: Fully containerized with Docker and Docker Compose for easy setup and consistent execution.
- **Asynchronous Ingestion**: The pipeline service ingests data in the background, allowing the API to respond immediately.
- **RESTful APIs**: Both the mock server and pipeline service expose clean, well-documented REST APIs for interaction and health monitoring.
- **Scalable Design**: The architecture allows for individual services to be scaled independently.
- **Automated Schema Creation**: The pipeline service automatically creates the required database table on startup.

## Architecture

The data flows through the system as follows:

```
┌─────────────┐      ┌──────────────────┐      ┌────────────────┐
│ Mock Server │      │ Pipeline Service │      │   PostgreSQL   │
│ (Flask API) │──────► (FastAPI Ingestion)├──────► (DB Storage)   │
└─────────────┘      └──────────────────┘      └────────────────┘
       ▲                    │
       │                    │
       └────────────────────┘
         (API for Querying)
```

## Project Structure

```
Customer-Data-Pipeline/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── data/customers.json
└── pipeline-service/
    ├── app.py
    ├── Dockerfile
    └── requirements.txt
```

## Setup and Usage

### Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- A tool for API testing, such as `curl` or Postman.

### Quick Start

1.  **Clone the repository** and navigate to the `customer-data-pipeline` directory.

2.  **Build and run the services** using Docker Compose:
    ```bash
    docker-compose up -d --build
    ```

3.  **Verify that all containers are running**:
    ```bash
    docker-compose ps
    ```

4.  **Check the health of the services**:
    ```bash
    curl http://localhost:5000/api/health
    curl http://localhost:8000/api/health
    ```

### End-to-End Test Flow

Follow these steps to test the complete data flow:

1.  **Verify the mock data API** is serving customer data:
    ```bash
    curl "http://localhost:5000/api/customers?page=1&limit=5"
    ```

2.  **Trigger the ingestion process**. This will start the background task to fetch data from the mock server and load it into PostgreSQL:
    ```bash
    curl -X POST http://localhost:8000/api/ingest
    ```

3.  **Wait a few seconds** for ingestion to complete, then **validate the stored records** by querying the pipeline service:
    ```bash
    curl "http://localhost:8000/api/customers?page=1&limit=5"
    ```

4.  **Fetch a single customer** by their ID to confirm data integrity:
    ```bash
    curl http://localhost:8000/api/customers/CUST001
    ```

### Stopping the Services

- To **stop all services**:
  ```bash
  docker-compose down
  ```
- To **stop services and remove the database volume** (deleting all stored data):
  ```bash
  docker-compose down -v
  ```

## API Documentation

### Mock Server (Flask)

Base URL: `http://localhost:5000`

| Method | Endpoint                      | Description                               |
| :----- | :---------------------------- | :---------------------------------------- |
| `GET`  | `/api/health`                 | Health check endpoint.                    |
| `GET`  | `/api/customers`              | Get a paginated list of customers.        |
| `GET`  | `/api/customers/{customer_id}`| Get a single customer by ID.              |

**Query Parameters for `/api/customers`**:
- `page` (integer, default: 1): The page number to retrieve.
- `limit` (integer, default: 10): The number of records per page.

### Pipeline Service (FastAPI)

Base URL: `http://localhost:8000`

| Method | Endpoint                      | Description                               |
| :----- | :---------------------------- | :---------------------------------------- |
| `GET`  | `/api/health`                 | Health check endpoint.                    |
| `POST` | `/api/ingest`                 | Triggers the data ingestion process.      |
| `GET`  | `/api/customers`              | Get a paginated list of stored customers. |
| `GET`  | `/api/customers/{customer_id}`| Get a single stored customer by ID.       |

## Database Schema

The `customers` table is created automatically by the pipeline service with the following schema:

```sql
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    date_of_birth VARCHAR(20),
    account_balance NUMERIC(15, 2),
    created_at TIMESTAMP
);
```

## Key Learnings

- **Microservices Design**: Gained experience in designing, building, and integrating decoupled services.
- **Containerization with Docker**: Mastered creating Dockerfiles and orchestrating multi-container applications with Docker Compose.
- **API Development**: Developed RESTful APIs using both Flask and FastAPI, understanding the trade-offs of each framework.
- **Data Engineering**: Implemented a complete ETL (Extract, Transform, Load) process, including data fetching, validation, and storage.
- **Database Management**: Worked with PostgreSQL in a containerized environment, including automated schema creation and data querying.

## Future Enhancements

- **Data Validation**: Implement robust data validation using Pydantic to handle malformed records gracefully.
- **Error Handling and Retries**: Add a retry mechanism for failed API calls and a dead-letter queue for records that fail to process.
- **Scalability**: Introduce a message queue (e.g., RabbitMQ, Kafka) between the services to improve scalability and resilience.
- **Enhanced Monitoring**: Integrate a monitoring solution like Prometheus and Grafana to track service health and performance metrics.
- **CI/CD Pipeline**: Set up a continuous integration and deployment pipeline to automate testing and deployments.

## About

This project was developed as a personal learning exercise to demonstrate proficiency in building data-driven applications with modern engineering practices.