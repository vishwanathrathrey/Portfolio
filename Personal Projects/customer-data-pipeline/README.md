# Real-Time Customer Data Pipeline

## Overview

This project implements a real-time data pipeline that simulates the processing of customer data from a mock data source into a structured data warehouse. The system is built using a modern data engineering stack, including Kafka for event streaming, Spark Streaming for real-time processing, and Cassandra as a NoSQL data store. The entire pipeline is containerized with Docker, making it a portable and scalable solution for handling streaming data.

## Recruiter Snapshot

This project demonstrates:
- **Real-Time Data Engineering:** Proficiency in designing and building an end-to-end, real-time data pipeline using industry-standard tools like Kafka and Spark Streaming.
- **Distributed Stream Processing:** Expertise in using Spark Streaming to consume, transform, and enrich data streams in a scalable and fault-tolerant manner.
- **Event-Driven Architecture:** Competency in building a system based on an event-driven architecture, with Kafka serving as the central message bus for decoupling data producers and consumers.
- **NoSQL Data Modeling:** Experience with Apache Cassandra, including designing a data model optimized for the high-write throughput required by streaming applications.
- **Containerization and Orchestration:** Skill in using Docker and Docker Compose to containerize and orchestrate a complex, multi-service data pipeline, ensuring reproducibility and ease of deployment.

## Features

- **Mock Data Generation:** A mock server that generates and streams realistic customer and transaction data to a Kafka topic.
- **Real-Time Ingestion with Kafka:** Apache Kafka is used as a distributed message queue to ingest high-throughput data streams.
- **Stream Processing with Spark:** A Spark Streaming job consumes data from Kafka, performs real-time transformations (e.g., data cleaning, enrichment), and writes the results to Cassandra.
- **NoSQL Data Warehouse:** Apache Cassandra is used as the final data store, optimized for fast writes and scalable reads.
- **Containerized Pipeline:** The entire pipeline, including the mock server, Kafka, Zookeeper, Spark, and Cassandra, is containerized and managed with Docker Compose.

## Architecture

The pipeline is composed of several containerized services that work in concert to process data in real time.

1.  **Mock Data Server:**
    - A simple Python-based server that generates fake customer and transaction data.
    - It acts as a data producer, sending JSON-formatted data records to a specific Kafka topic.

2.  **Kafka Cluster:**
    - A single-node Kafka cluster (with Zookeeper) serves as the backbone of the pipeline.
    - It ingests the streaming data from the mock server and makes it available for consumption by downstream processors.

3.  **Spark Streaming Processor:**
    - A Spark Streaming application connects to the Kafka topic and consumes the data in micro-batches.
    - It parses the JSON data, applies transformations (e.g., joining customer and transaction data, calculating new fields), and cleans the data.
    - The processed data is then written to a Cassandra table.

4.  **Cassandra Database:**
    - A Cassandra node acts as the data warehouse for the structured, processed data.
    - The data model is designed to support efficient queries and high-velocity writes from the Spark Streaming job.

## Project Workflow

1.  The `mock-server` starts generating customer and transaction data and streams it to the `customer_data` Kafka topic.
2.  The `pipeline-service` (Spark Streaming) consumes the raw data from the Kafka topic.
3.  Inside the Spark job, the streaming data is cleaned, enriched, and transformed into a structured format.
4.  The processed data is continuously written to the `customers` table in the Cassandra database.
5.  A data analyst or downstream application can then query the Cassandra database to get real-time insights into customer activity.

## Techniques and Concepts Applied

| Technique | Application |
|---|---|
| **Event Streaming** | Using Kafka as a durable, scalable message broker for real-time data ingestion. |
| **Stream Processing** | Using Spark Streaming to perform stateful and stateless transformations on data in motion. |
| **NoSQL Data Modeling** | Designing a schema in Cassandra optimized for high-write throughput and time-series data. |
| **Containerization** | Using Docker to isolate each component of the pipeline (Kafka, Spark, Cassandra). |
| **Orchestration** | Using Docker Compose to define and manage the multi-container application. |
| **Data Serialization** | Handling data serialization and deserialization between services (JSON). |

## Key Learnings

- **Decoupling with Kafka:** Kafka proved to be essential for decoupling the data producer from the consumer, allowing each to operate and scale independently.
- **Spark Streaming for Complex Logic:** Spark Streaming was powerful enough to handle complex transformations and enrichments in real time, which would be difficult with simpler stream processors.
- **Cassandra for Write-Intensive Workloads:** Cassandra's architecture is perfectly suited for the high-volume, continuous writes generated by a streaming pipeline.
- **Challenges of Multi-Container Networking:** Setting up the network connections between the different containers in Docker Compose required careful configuration to ensure services could communicate correctly.

## Future Work

- **Deployment to Kubernetes:** Migrate the Docker Compose setup to a Kubernetes cluster for better scalability, fault tolerance, and production readiness.
- **Real-Time Analytics Dashboard:** Build a dashboard (e.g., with Streamlit or Dash) that queries Cassandra to provide real-time visualizations of customer activity.
- **Schema Management:** Integrate a schema registry (e.g., Confluent Schema Registry) to enforce data schemas and prevent data quality issues.
- **Data Quality Monitoring:** Add a monitoring component to track data quality metrics and alert on anomalies in the stream.

## Repository Structure

```
Customer-Data-Pipeline/
├── mock-server/            # Mock data generator and Kafka producer
│   ├── Dockerfile
│   └── server.py
├── pipeline-service/       # Spark Streaming consumer and processor
│   ├── Dockerfile
│   └── stream_processor.py
└── docker-compose.yml      # Docker Compose file to orchestrate the pipeline
```

## Notes
- This project is a practical demonstration of building a real-time data engineering pipeline, showcasing skills that are highly relevant for modern data-intensive applications.
