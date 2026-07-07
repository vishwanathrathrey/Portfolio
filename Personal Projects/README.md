# Personal Projects

This directory contains personal projects focused on applying software engineering principles to Machine Learning, Data Engineering, and Generative AI problems. These projects demonstrate experience building APIs, ETL pipelines, containerized applications, ML-powered services, and LLM-integrated workflows.

Each project folder contains a dedicated `README.md` with detailed information on the architecture, setup, and usage.

## Projects

### [AI Code Review System](./AI-Code-Review/)

An automated, AI-powered platform that analyzes GitHub pull request diffs to detect bugs, security vulnerabilities, and code quality issues. The system validates findings against code evidence and generates comprehensive review reports in multiple formats. Currently triggered via a Flask REST API endpoint, the architecture is designed to be webhook-ready for seamless GitHub integration.

**Key Technologies**: Python, Flask, OpenAI API, GitHub REST API, SMTP, Markdown, HTML

**Key Skills**: LLM Integration, API Design, Pipeline Architecture, Security Scanning, Automated Reporting

---

### [Credit Risk ML System](./Credit-Risk-ML-System/)

An end-to-end local machine learning application for predicting credit risk using the Home Credit Default Risk dataset. The system combines PySpark-based data processing, Scikit-learn model training, FastAPI backend serving, and a React-based frontend dashboard. The entire application is containerized using Docker for easy local deployment.

**Key Technologies**: Python, PySpark, Scikit-learn, FastAPI, React, Docker, PostgreSQL

**Key Skills**: End-to-End ML Pipeline, Data Engineering, Model Serving, Frontend-Backend Integration, Containerization

---

### [Customer Data Pipeline](./Customer-Data-Pipeline/)

A containerized, end-to-end data pipeline that ingests customer data from a mock API, processes it, and stores it in a PostgreSQL database. The project demonstrates a microservices architecture using Flask (mock server), FastAPI (pipeline service), and Docker Compose for orchestration.

**Key Technologies**: Python, Flask, FastAPI, PostgreSQL, Docker, Docker Compose

**Key Skills**: Microservices Architecture, ETL Pipeline Design, REST API Development, Container Orchestration, Database Integration

---

## Key Skills Demonstrated

| Domain | Skills |
|--------|--------|
| **Machine Learning** | Model Training, Feature Engineering, Model Evaluation, Scikit-learn Pipelines |
| **Data Engineering** | PySpark Processing, ETL Pipelines, Data Validation, Database Integration |
| **AI & LLMs** | LLM Integration, Prompt Engineering, AI Output Normalization, AI-Assisted Code Analysis |
| **Software Engineering** | API Design, Microservices, Docker Containerization, Pipeline Architecture |
| **Full-Stack Development** | FastAPI Backend, React Frontend, RESTful APIs, Frontend-Backend Integration |

## Project Highlights

### AI Code Review System
- **AI-Powered Analysis**: Leverages LLMs for deep code analysis across multiple issue categories
- **Evidence Validation**: Cross-references findings against actual code diffs to reduce false positives
- **Security Scanning**: Dual-layer analysis combining AI review with dedicated security vulnerability scanning
- **Multi-Format Reporting**: Generates professional reports in Markdown, HTML, and plain text
- **Webhook-Ready Architecture**: Designed for future GitHub webhook integration with minimal changes

### Credit Risk ML System
- **End-to-End ML Pipeline**: Complete workflow from data processing to model deployment
- **PySpark Preprocessing**: Efficient data cleaning, transformation, and feature engineering on large datasets
- **FastAPI Serving**: Production-ready API for real-time predictions with health and metrics endpoints
- **React Dashboard**: User-friendly interface for entering applicant data and viewing predictions
- **Docker-Based Deployment**: Containerized services for consistent local deployment across environments

### Customer Data Pipeline
- **Microservices Architecture**: Decoupled services for data generation, processing, and storage
- **Containerized Deployment**: Fully containerized with Docker and Docker Compose for easy setup
- **Asynchronous Ingestion**: Background data ingestion allowing API to respond immediately
- **Automated Schema Creation**: Automatic database table creation on service startup
- **Scalable Design**: Architecture supports independent scaling of individual services

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| **Languages** | Python 3.x, TypeScript, JavaScript |
| **ML & Data** | PySpark, Scikit-learn, Pandas, NumPy |
| **AI & LLMs** | OpenAI API, Prompt Engineering |
| **Backend** | FastAPI, Flask, REST APIs |
| **Frontend** | React, Vite, HTML, CSS |
| **Databases** | PostgreSQL |
| **Containerization** | Docker, Docker Compose |
| **Version Control** | Git, GitHub REST API |
| **Testing** | Postman |

---

## Project Structure

Personal-Projects/
├── AI-Code-Review/
│ ├── app/
│ ├── reports/
│ ├── reviews/
│ ├── webhook_server.py
│ └── README.md
├── Credit-Risk-ML-System/
│ ├── api/
│ ├── ml/
│ ├── pyspark/
│ ├── frontend/
│ ├── docker-compose.yml
│ ├── Dockerfile
│ └── README.md
├── Customer-Data-Pipeline/
│ ├── mock-server/
│ ├── pipeline-service/
│ ├── docker-compose.yml
│ └── README.md
└── README.md


---

## Learning Outcomes

### 1. End-to-End System Design
Building complete systems from data ingestion to deployment taught the importance of component integration, data validation, and error handling across distributed services.

### 2. Microservices vs. Monolith
Experience with both approaches: the Credit Risk ML System follows a modular monolith with separated concerns, while the Customer Data Pipeline demonstrates true microservices with independent scaling and deployment.

### 3. LLM Integration Challenges
Working with LLMs introduced challenges in output normalization, prompt engineering, and validation. Understanding how to parse, validate, and structure AI-generated content for reliable downstream processing was critical.

### 4. Containerization Benefits
Docker and Docker Compose significantly simplified dependency management and deployment. Consistent environments across development, testing, and production reduced integration issues.

### 5. API-First Design
Designing APIs first (contract-first development) improved system design and enabled parallel development of frontend and backend services. Well-documented APIs are essential for maintainable systems.

### 6. Data Processing Patterns
PySpark enabled efficient processing of large datasets, while Scikit-learn provided production-ready machine learning pipelines. Understanding when to use each tool is essential for scalable data systems.

---

## Notes

- Each project folder contains a comprehensive README with setup instructions, architecture diagrams, and API documentation
- Docker-based projects can be started with a single command: `docker-compose up`
- Projects are designed to run locally and can be extended for cloud deployment
- Source code is available for collaboration and review

---

## About

This portfolio represents personal projects undertaken to explore and demonstrate practical application of machine learning, data engineering, and software engineering concepts. Each project addresses a real-world problem and follows professional development practices including version control, documentation, and containerization.

---

## Contact

For questions, collaboration opportunities, or demonstrations, please reach out via GitHub or the contact information available on my portfolio.