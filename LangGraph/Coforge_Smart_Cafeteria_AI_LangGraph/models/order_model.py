from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class FoodItemRequest(BaseModel):

    food_name: str = Field(min_length=1)
    quantity: int = Field(gt=0)


class OrderRequest(BaseModel):

    employee_id: str = Field(min_length=1)
    employee_name: str = Field(min_length=1)
    items: list[FoodItemRequest] = Field(min_length=1)


class InvoiceItem(BaseModel):

    food_name: str
    quantity: int
    unit_price: float
    amount: float


class InvoiceResponse(BaseModel):

    invoice_number: str
    order_id: str
    employee_id: str
    employee_name: str
    status: str
    items: list[InvoiceItem]
    subtotal: float
    gst_percentage: float
    gst_amount: float
    total_payable: float
    expected_preparation_minutes: int


class OrderResponse(BaseModel):

    order_id: str
    invoice: InvoiceResponse
    created_at: datetime


class DelayCheckResponse(BaseModel):

    order_id: str
    employee_id: str
    elapsed_minutes: int
    expected_minutes: int
    delay_minutes: int
    priority: Literal["NORMAL", "HIGH", "CRITICAL"]
    escalated_to: str
    message: str


class EscalationAnswer(BaseModel):

    priority: Literal["NORMAL", "HIGH", "CRITICAL"]
    recipient: str
    message: str
