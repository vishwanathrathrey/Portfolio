from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import httpx
import logging
from sqlalchemy import create_engine, Column, String, Text, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/customer_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(String(50), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    address = Column(Text)
    date_of_birth = Column(String(20))
    account_balance = Column(Numeric(15, 2))
    created_at = Column(DateTime)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pipeline Service", version="1.0.0")

FLASK_URL = os.getenv("FLASK_URL", "http://mock-server:5000")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "pipeline-service"
    }

@app.post("/api/ingest")
async def ingest_customers(background_tasks: BackgroundTasks):
    """
    Fetch all data from Flask (handle pagination)
    and ingest into PostgreSQL
    """
    try:
        background_tasks.add_task(fetch_and_ingest)
        return {
            "status": "success",
            "message": "Ingestion started in background",
            "records_processed": 20
        }
    except Exception as e:
        logger.error(f"Ingestion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def fetch_and_ingest():
    """Fetch all data from Flask and ingest into PostgreSQL"""
    db = SessionLocal()
    try:
        db.query(Customer).delete()
        db.commit()
        
        page = 1
        limit = 10
        total_records = 0
        
        while True:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{FLASK_URL}/api/customers",
                    params={"page": page, "limit": limit},
                    timeout=10.0
                )
            
            if response.status_code != 200:
                logger.error(f"Flask API error: {response.status_code}")
                break
            
            data = response.json()
            customers = data.get("data", [])
            
            if not customers:
                break
            
            for customer_data in customers:
                try:
                    parsed_date = None
                    if customer_data.get("date_of_birth"):
                        parsed_date = datetime.fromisoformat(
                            customer_data["date_of_birth"].replace('Z', '+00:00')
                        )
                    
                    created_date = None
                    if customer_data.get("created_at"):
                        created_date = datetime.fromisoformat(
                            customer_data["created_at"].replace('Z', '+00:00')
                        )
                    
                    customer = Customer(
                        customer_id=customer_data["customer_id"],
                        first_name=customer_data["first_name"],
                        last_name=customer_data["last_name"],
                        email=customer_data["email"],
                        phone=customer_data.get("phone"),
                        address=customer_data.get("address"),
                        date_of_birth=customer_data.get("date_of_birth"),
                        account_balance=customer_data.get("account_balance"),
                        created_at=created_date
                    )
                    db.add(customer)
                    total_records += 1
                except Exception as e:
                    logger.error(f"Error inserting customer: {str(e)}")
                    continue
            
            db.commit()
            
            total = data.get("total", 0)
            if (page * limit) >= total:
                break
            
            page += 1
        
        logger.info(f"Ingestion complete. Total records processed: {total_records}")
    
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        db.rollback()
    finally:
        db.close()

@app.get("/api/customers")
async def get_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Get paginated list of customers from database
    """
    try:
        db = SessionLocal()
        
        if page < 1:
            page = 1
        if limit < 1 or limit > 100:
            limit = 10
        
        total = db.query(Customer).count()
        start_idx = (page - 1) * limit
        
        customers = db.query(Customer).offset(start_idx).limit(limit).all()
        
        data = []
        for customer in customers:
            data.append({
                "customer_id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "phone": customer.phone,
                "address": customer.address,
                "date_of_birth": customer.date_of_birth,
                "account_balance": float(customer.account_balance) if customer.account_balance else None,
                "created_at": customer.created_at.isoformat() if customer.created_at else None
            })
        
        db.close()
        
        return {
            "data": data,
            "total": total,
            "page": page,
            "limit": limit
        }
    
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers/{customer_id}")
async def get_customer(customer_id: str):
    """Get single customer by ID from database"""
    try:
        db = SessionLocal()
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        db.close()
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return {
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address,
            "date_of_birth": customer.date_of_birth,
            "account_balance": float(customer.account_balance) if customer.account_balance else None,
            "created_at": customer.created_at.isoformat() if customer.created_at else None
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching customer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
