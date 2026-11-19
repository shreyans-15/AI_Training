from sqlalchemy import Column,Integer,String,Numeric,Boolean,Date
from config.database import Base

class BankCustomer(Base):
    __tablename__="BankCustomer"

    customer_id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    customer_name=Column(String(100),nullable=False)
    email=Column(String(100),unique=True,nullable=False)
    account_number=Column(String(30),unique=True,nullable=False)
    account_type=Column(String(20),nullable=False)
    branch_name=Column(String(100),nullable=False)
    balance=Column(Numeric(12,2),nullable=False)
    is_active=Column(Boolean,default=True)
    opened_on=Column(Date,nullable=False)
