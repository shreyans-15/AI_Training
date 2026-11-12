 
from sqlalchemy.orm import Session
from sqlalchemy import func
 
from models.employeeperformance_model import EmployeePerformance
from schemas.employeeperformance_schema import (
    EmployeePerformanceCreate,
    EmployeePerformanceUpdate
)
 
# 1. Create employee performance record
def create_employee(db: Session, employee: EmployeePerformanceCreate):
 
    db_employee = EmployeePerformance(**employee.model_dump())
 
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
 
    return db_employee
 
# 2. Get all employee records with pagination
def get_all_employees(db: Session, skip: int = 0, limit: int = 10):
 
    return (
        db.query(EmployeePerformance)
        .offset(skip)
        .limit(limit)
        .all()
    )
 
# 3. Get employee by employee ID
def get_employee_by_id(db: Session, employee_id: int):
 
    return (
        db.query(EmployeePerformance)
        .filter(EmployeePerformance.employee_id == employee_id)
        .first()
    )
 
# 4. Update employee performance details
def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeePerformanceUpdate
):
 
    db_employee = get_employee_by_id(db, employee_id)
 
    if db_employee:
        update_data = employee_data.model_dump()
 
        for key, value in update_data.items():
            setattr(db_employee, key, value)
 
        db.commit()
        db.refresh(db_employee)
 
    return db_employee
 
# 5. Delete employee record
def delete_employee(db: Session, employee_id: int):
 
    db_employee = get_employee_by_id(db, employee_id)
 
    if db_employee:
        db.delete(db_employee)
        db.commit()
 
    return db_employee
 
# 6. Get employees by department
def get_employees_by_department(db: Session, department: str):
 
    return (
        db.query(EmployeePerformance)
        .filter(EmployeePerformance.department == department)
        .all()
    )
 
# 7. Get employees with rating >= 4
def get_high_performers(db: Session):
 
    return (
        db.query(EmployeePerformance)
        .filter(EmployeePerformance.performance_rating >= 4)
        .all()
    )
 
# 8. Get average performance rating by department
def get_department_average(db: Session):
 
    return (
        db.query(
            EmployeePerformance.department,
            func.avg(EmployeePerformance.performance_rating).label(
                "average_rating"
            )
        )
        .group_by(EmployeePerformance.department)
        .all()
    )
 
# 9. Get five highest-rated employees
def get_top_five_employees(db: Session):
 
    return (
        db.query(EmployeePerformance)
        .order_by(EmployeePerformance.performance_rating.desc())
        .limit(5)
        .all()
    )
 
# 10. Classify employee performance
def get_performance_classification(db: Session):
 
    employees = db.query(EmployeePerformance).all()
 
    result = []
 
    for employee in employees:
 
        if employee.performance_rating >= 4.5:
            category = "Outstanding"
 
        elif employee.performance_rating >= 3.5:
            category = "Good"
 
        else:
            category = "Needs Improvement"
 
        result.append({
            "employee_id": employee.employee_id,
            "employee_name": employee.employee_name,
            "performance_rating": employee.performance_rating,
            "classification": category
        })
 
    return result
 