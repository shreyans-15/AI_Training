from datetime import date
from decimal import Decimal
from pydantic import BaseModel,EmailStr,Field,ConfigDict
from typing import Literal

class BankCustomerBase(BaseModel):
    customer_name:str
    email:EmailStr
    account_number:str
    account_type:Literal["Savings","Current"]
    branch_name:str
    balance:Decimal=Field(ge=0)
    is_active:bool=True
    opened_on:date

class BankCustomerCreate(BankCustomerBase):
    pass

class BankCustomerUpdate(BaseModel):
    customer_name:str
    branch_name:str

class AmountSchema(BaseModel):
    amount:Decimal=Field(gt=0)

class BankCustomerResponse(BankCustomerBase):
    customer_id:int
    model_config=ConfigDict(from_attributes=True)
