# Backend Developer Technical Assessment - Data Pipeline

A complete data pipeline with 3 Docker services: Flask API mock server, FastAPI ingestion pipeline, and PostgreSQL database.

## Project Overview

This project implements a data pipeline that:
1. **Flask Mock Server** (Port 5000): Serves customer data from a JSON file with pagination support
2. **FastAPI Pipeline Service** (Port 8000): Ingests customer data from Flask into PostgreSQL, with full CRUD endpoints
3. **PostgreSQL Database** (Port 5432): Stores customer data persistently

### Data Flow

```
Flask (JSON) → FastAPI (Ingestion) → PostgreSQL (Storage)
```

## Project Structure

```
project-root/
├── docker-compose.yml          # Orchestrates all services
├── README.md                   # This file
├── mock-server/
│   ├── app.py                  # Flask application
│   ├── data/
│   │   └── customers.json      # Customer data (20+ records)
│   ├── Dockerfile              # Flask Docker image
│   └── requirements.txt         # Flask dependencies
└── pipeline-service/
    ├── app.py                  # FastAPI application
    ├── Dockerfile              # FastAPI Docker image
    └── requirements.txt         # FastAPI dependencies
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- curl (for testing endpoints)

### Installation & Running

1. **Clone/Navigate to project directory:**
   ```bash
   cd assignment
   ```

2. **Start all services:**
   ```bash
   docker-compose up -d
   ```

3. **Verify all services are running:**
   ```bash
   docker-compose ps
   ```

4. **Check service health:**
   ```bash
   curl http://localhost:5000/api/health    # Flask
   curl http://localhost:8000/api/health    # FastAPI
   ```

### Stopping Services

```bash
docker-compose down
```

To also remove volumes:
```bash
docker-compose down -v
```

## API Endpoints

### Mock Server (Flask) - Port 5000

#### GET /api/customers
Retrieve paginated list of customers

**Parameters:**
- `page` (int, default=1): Page number
- `limit` (int, default=10): Records per page (max 100)

**Example:**
```bash
curl "http://localhost:5000/api/customers?page=1&limit=5"
```

**Response:**
```json
{
  "data": [
    {
      "customer_id": "CUST001",
      "first_name": "John",
      "last_name": "Smith",
      "email": "john.smith@example.com",
      "phone": "5551234567",
      "address": "123 Main St, Springfield, IL 62701",
      "date_of_birth": "1985-03-15",
      "account_balance": 5432.50,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 20,
  "page": 1,
  "limit": 5
}
```

#### GET /api/customers/{id}
Retrieve single customer by ID

**Example:**
```bash
curl http://localhost:5000/api/customers/CUST001
```

**Response:**
```json
{
  "customer_id": "CUST001",
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@example.com",
  "phone": "5551234567",
  "address": "123 Main St, Springfield, IL 62701",
  "date_of_birth": "1985-03-15",
  "account_balance": 5432.50,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Response (404):**
```json
{
  "error": "Customer not found"
}
```

#### GET /api/health
Health check endpoint

**Example:**
```bash
curl http://localhost:5000/api/health
```

---

### Pipeline Service (FastAPI) - Port 8000

#### POST /api/ingest
Fetch all customer data from Flask and ingest into PostgreSQL

**Example:**
```bash
curl -X POST http://localhost:8000/api/ingest
```

**Response:**
```json
{
  "status": "success",
  "message": "Ingestion started in background",
  "records_processed": 20
}
```

#### GET /api/customers
Retrieve paginated list of customers from database

**Parameters:**
- `page` (int, default=1): Page number
- `limit` (int, default=10): Records per page

**Example:**
```bash
curl "http://localhost:8000/api/customers?page=1&limit=5"
```

**Response:**
```json
{
  "data": [
    {
      "customer_id": "CUST001",
      "first_name": "John",
      "last_name": "Smith",
      "email": "john.smith@example.com",
      "phone": "5551234567",
      "address": "123 Main St, Springfield, IL 62701",
      "date_of_birth": "1985-03-15",
      "account_balance": 5432.50,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 20,
  "page": 1,
  "limit": 5
}
```

#### GET /api/customers/{id}
Retrieve single customer from database by ID

**Example:**
```bash
curl http://localhost:8000/api/customers/CUST001
```

**Response:**
```json
{
  "customer_id": "CUST001",
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@example.com",
  "phone": "5551234567",
  "address": "123 Main St, Springfield, IL 62701",
  "date_of_birth": "1985-03-15",
  "account_balance": 5432.50,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Response (404):**
```json
{
  "error": "Customer not found"
}
```

#### GET /api/health
Health check endpoint

**Example:**
```bash
curl http://localhost:8000/api/health
```

---

## Database Schema

### Customers Table

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

### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| customer_id | VARCHAR(50) | Unique customer identifier (Primary Key) |
| first_name | VARCHAR(100) | Customer's first name |
| last_name | VARCHAR(100) | Customer's last name |
| email | VARCHAR(255) | Customer's email address |
| phone | VARCHAR(20) | Customer's phone number |
| address | TEXT | Customer's street address |
| date_of_birth | VARCHAR(20) | Customer's date of birth (ISO format) |
| account_balance | NUMERIC(15,2) | Customer's account balance with 2 decimals |
| created_at | TIMESTAMP | Account creation timestamp |

---

## Testing Workflow

### Complete Testing Flow

```bash
# 1. Start all services
docker-compose up -d

# 2. Verify Flask mock server is serving data
curl "http://localhost:5000/api/customers?page=1&limit=5"

# 3. Trigger data ingestion from FastAPI
curl -X POST http://localhost:8000/api/ingest

# 4. Verify data was ingested into database
curl "http://localhost:8000/api/customers?page=1&limit=5"

# 5. Test single customer retrieval
curl http://localhost:8000/api/customers/CUST001

# 6. Test health checks
curl http://localhost:5000/api/health
curl http://localhost:8000/api/health
```

---

## Environment Variables

### Flask Mock Server
- `FLASK_ENV`: Environment (default: production)

### FastAPI Pipeline Service
- `DATABASE_URL`: PostgreSQL connection string
  - Format: `postgresql://username:password@host:port/database`
  - Default: `postgresql://postgres:password@postgres:5432/customer_db`
- `FLASK_URL`: Flask mock server URL
  - Format: `http://hostname:port`
  - Default: `http://mock-server:5000`

### PostgreSQL
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: password)
- `POSTGRES_DB`: Database name (default: customer_db)

---

## Data Characteristics

### Customer Data
- **Total Records:** 20+ customers
- **Fields:** customer_id, first_name, last_name, email, phone, address, date_of_birth, account_balance, created_at
- **Format:** JSON with proper data types
- **Location:** `mock-server/data/customers.json`

### Pagination
- Default page size: 10 records
- Maximum page size: 100 records
- Supports unlimited pages

---

## Error Handling

### Common Error Scenarios

**404 - Customer Not Found**
```json
{
  "error": "Customer not found"
}
```

**400 - Bad Request**
```json
{
  "error": "Invalid pagination parameters"
}
```

**500 - Internal Server Error**
```json
{
  "error": "Database connection failed"
}
```

---

## Code Quality Features

### Flask (Mock Server)
- ✅ Clean architecture with separation of concerns
- ✅ Proper error handling with HTTP status codes
- ✅ Pagination validation and limits
- ✅ JSON data loading from file
- ✅ Health check endpoint
- ✅ Logging support

### FastAPI (Pipeline Service)
- ✅ Async/await support for background tasks
- ✅ SQLAlchemy ORM for database operations
- ✅ Async HTTP client for Flask communication
- ✅ Proper exception handling and logging
- ✅ Database connection pooling
- ✅ Type hints for all functions
- ✅ Pagination with validation
- ✅ Upsert logic for data consistency
- ✅ Health checks with proper status codes

### Docker
- ✅ Multi-stage build optimization
- ✅ Proper service dependency management
- ✅ Health checks for container orchestration
- ✅ Environment variable configuration
- ✅ Persistent volume for database
- ✅ Bridge network for service communication
- ✅ Slim base images for reduced image size

---

## Performance Considerations

### Pagination
- Pagination is implemented to handle large datasets efficiently
- Queries are limited to prevent memory overload
- Default limit of 10 and max limit of 100 records per page

### Database
- PostgreSQL with connection pooling
- Indexed primary key for fast lookups
- Persistent volume to preserve data between restarts

### Async Processing
- Background tasks for data ingestion to avoid blocking
- Async HTTP client for non-blocking Flask API calls

---

## Troubleshooting

### Services not starting?
```bash
# Check logs
docker-compose logs -f

# Check specific service
docker-compose logs flask  # or pipeline-service, postgres
```

### Cannot connect to database?
```bash
# Verify PostgreSQL is healthy
docker-compose ps

# Check database connection
docker-compose exec postgres psql -U postgres -d customer_db -c "SELECT COUNT(*) FROM customers;"
```

### Data not ingested?
```bash
# Check if ingestion endpoint was called
curl -X POST http://localhost:8000/api/ingest

# Wait a moment for background processing, then check data
curl http://localhost:8000/api/customers
```

### Port conflicts?
If ports are already in use, modify docker-compose.yml:
```yaml
ports:
  - "5001:5000"  # Use 5001 instead of 5000
```

---

## Deployment Notes

### Production Considerations
- Change default PostgreSQL password
- Use environment variables for sensitive data
- Implement API authentication/authorization
- Add rate limiting and request validation
- Use a production-grade ASGI server (Gunicorn)
- Configure proper logging and monitoring
- Use database migrations for schema management
- Implement backup and disaster recovery

---

## Submission Checklist

- ✅ All 3 services start with `docker-compose up`
- ✅ Flask mock server serves paginated customer data on port 5000
- ✅ FastAPI pipeline service ingests data successfully
- ✅ All API endpoints working:
  - ✅ GET /api/customers (paginated)
  - ✅ GET /api/customers/{id} (single customer)
  - ✅ POST /api/ingest (data ingestion)
  - ✅ GET /api/health (health checks)
- ✅ PostgreSQL stores customer data
- ✅ Docker Compose properly configured with dependencies and networking
- ✅ Comprehensive documentation
- ✅ Clean, well-structured code
- ✅ Error handling implemented

---

## Support

For issues or questions, check:
1. Docker Compose logs: `docker-compose logs -f`
2. Service health: `curl http://localhost:PORT/api/health`
3. Database connectivity using psql:
   ```bash
   docker-compose exec postgres psql -U postgres -d customer_db
   ```

---

## License

This is an assessment project for educational purposes.
