from sqlalchemy import select,func
from sqlalchemy.orm import Session
from models.bankcustomer_model import BankCustomer

def add_customer(db,data):
    customer=BankCustomer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def get_all_customers(db,skip=0,limit=10):
    return db.scalars(select(BankCustomer).offset(skip).limit(limit)).all()

def get_by_account(db,account_number):
    return db.scalar(select(BankCustomer).where(BankCustomer.account_number==account_number))

def update_customer(db,customer_id,data):
    customer=db.get(BankCustomer,customer_id)
    if not customer: return None
    for k,v in data.model_dump().items():
        setattr(customer,k,v)
    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(db,customer_id):
    customer=db.get(BankCustomer,customer_id)
    if not customer: return False
    db.delete(customer)
    db.commit()
    return True
