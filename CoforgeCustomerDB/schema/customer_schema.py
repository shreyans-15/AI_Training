from pydantic import (
    BaseModel, Field, EmailStr, ConfigDict
)


class CustomerBase(BaseModel):
    customer_name: str = Field(min_length=2)
    email: EmailStr
    age: int = Field(gt=15, lt=100)
    gender: str = Field(min_length=2)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    customer_id: int

    model_config = ConfigDict(from_attributes=True)