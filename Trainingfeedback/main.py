from fastapi import FastAPI
from services import employee_service as service
from config.database import Base,SessionLocal,engine
from schemas.employee_schema import EmployeeResponse

app = FastAPI(
    title = "My first API service",
    version = "1.0.1"
)

Base.metadata.create_all(bind = engine)

@app.get("/")
def home():
    return{
        "message" : "Hello"
    }
@app.get("/employees",response_model = list[EmployeeResponse])

def get_all_employee():
    db = SessionLocal()
    return service.get_all_employees(db)

#@app.post("/employees")
#def create_employee(employee: EmployeeCreate):
#    db = SessionLocal()
#    return service.create_employee(db, employee)

@app.get("/employees/{id}",response_model=EmployeeResponse)
def getemployeebyid(id: int):
   
    db=SessionLocal()
    return service.get_employee_by_id(db,id)
 
@app.post("/employees",response_model=EmployeeResponse)
def createemployee( employee: EmployeeCreate):
    db=SessionLocal()
    return service.add_employee(db,employee)