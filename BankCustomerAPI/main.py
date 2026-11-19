from fastapi import FastAPI,HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal,engine,Base
from services import bankcustomer_service as service
from schema.bankcustomer_schema import BankCustomerCreate,BankCustomerUpdate,BankCustomerResponse

app=FastAPI(title="Bank Customer API",version="1.0")
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message":"Bank Customer API"}

@app.post("/customers",response_model=BankCustomerResponse)
def create_customer(customer:BankCustomerCreate):
    db=SessionLocal()
    return service.add_customer(db,customer)

@app.get("/customers",response_model=list[BankCustomerResponse])
def get_customers(page:int=1,size:int=10):
    db=SessionLocal()
    return service.get_all_customers(db,(page-1)*size,size)

@app.get("/customers/{account_number}")
def get_customer(account_number:str):
    db=SessionLocal()
    data=service.get_by_account(db,account_number)
    if not data:
        raise HTTPException(status_code=404,detail="Account not found")
    return data
