from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
 
from config.database import engine, Base, get_db
from config.logging_config import logger
 
from models.employeeperformance_model import EmployeePerformance
 
from schemas.employeeperformance_schema import (
    EmployeePerformanceCreate,
    EmployeePerformanceResponse
)
 
from services import employeeperformance_service as service
 
# Create database tables
Base.metadata.create_all(bind=engine)
 
# Initialize FastAPI application
app = FastAPI(
    title="Employee Performance Management API",
    description="API for managing employee performance records",
    version="1.0.0"
)
 
@app.get("/")
def home():
 
    return {
        "message": "Employee Performance Management API is running"
    }
 
# 1. Create employee performance record
@app.post(
    "/employees/",
    response_model=EmployeePerformanceResponse,
    status_code=201
)
def create_employee(
    employee: EmployeePerformanceCreate,
    db: Session = Depends(get_db)
):
 
    try:
        new_employee = service.create_employee(db, employee)

        logger.info(
            "Employee record created successfully. Employee ID: %s",
            new_employee.employee_id
        )

        return new_employee

    except IntegrityError:

        db.rollback()

        logger.warning(
            "Attempt to create duplicate employee ID: %s",
            employee.employee_id
        )

        raise HTTPException(
            status_code=409,
            detail="Employee ID already exists"
        )