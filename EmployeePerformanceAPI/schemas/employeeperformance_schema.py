 
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
 
# Common fields used when creating an employee record
class EmployeePerformanceBase(BaseModel):
 
    employee_name: str = Field(min_length=1, max_length=100)
    department: str = Field(min_length=1, max_length=100)
    designation: str = Field(min_length=1, max_length=100)
 
    salary: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
 
    performance_rating: float = Field(ge=1, le=5)
 
    projects_completed: int = Field(ge=0)
 
    attendance_percentage: float = Field(ge=0, le=100)
 
    review_year: int
 
# Schema for creating a new employee record
class EmployeePerformanceCreate(EmployeePerformanceBase):
 
    employee_id: int = Field(gt=0)
 
# Schema for updating an employee record
class EmployeePerformanceUpdate(BaseModel):
 
    performance_rating: float = Field(ge=1, le=5)
 
    attendance_percentage: float = Field(ge=0, le=100)
 
    projects_completed: int = Field(ge=0)
 
# Schema for sending employee data in API responses
class EmployeePerformanceResponse(EmployeePerformanceBase):
 
    employee_id: int
 
    model_config = ConfigDict(from_attributes=True)
 