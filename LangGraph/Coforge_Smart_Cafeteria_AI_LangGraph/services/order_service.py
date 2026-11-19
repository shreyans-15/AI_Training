import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

from models.order_model import (
    OrderRequest,
    OrderResponse,
    InvoiceResponse,
    InvoiceItem
)

BASE_DIR = Path(__file__).resolve().parents[1]
MENU_PATH = BASE_DIR / "config" / "menu.json"

with MENU_PATH.open("r", encoding="utf-8") as menu_file:
    MENU = json.load(menu_file)

ORDERS = {}
ORDER_COUNTER = 1000
INVOICE_COUNTER = 1000
ORDER_LOCK = Lock()

EXPECTED_PREPARATION_MINUTES = 20
GST_PERCENTAGE = 5


def validate_order(request: OrderRequest):
    if not request.employee_id.strip():
        raise ValueError("Employee ID cannot be empty.")

    if not request.employee_name.strip():
        raise ValueError("Employee name cannot be empty.")

    validated_items = []

    for item in request.items:
        food_name = item.food_name.strip()

        if food_name not in MENU:
            raise ValueError(
                f"'{food_name}' is not available in the cafeteria menu."
            )

        if item.quantity <= 0:
            raise ValueError("Food quantity must be greater than zero.")

        validated_items.append({
            "food_name": food_name,
            "quantity": item.quantity,
            "unit_price": float(MENU[food_name])
        })

    return validated_items


def generate_invoice(request: OrderRequest, validated_items):
    global INVOICE_COUNTER

    invoice_items = []
    subtotal = 0.0

    for item in validated_items:
        amount = round(item["unit_price"] * item["quantity"], 2)
        subtotal += amount

        invoice_items.append(
            InvoiceItem(
                food_name=item["food_name"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                amount=amount
            )
        )

    subtotal = round(subtotal, 2)
    gst_amount = round(subtotal * GST_PERCENTAGE / 100, 2)
    total_payable = round(subtotal + gst_amount, 2)

    with ORDER_LOCK:
        INVOICE_COUNTER += 1
        invoice_number = f"INV{INVOICE_COUNTER}"

    return InvoiceResponse(
        invoice_number=invoice_number,
        order_id="",
        employee_id=request.employee_id,
        employee_name=request.employee_name,
        status="Order Placed",
        items=invoice_items,
        subtotal=subtotal,
        gst_percentage=GST_PERCENTAGE,
        gst_amount=gst_amount,
        total_payable=total_payable,
        expected_preparation_minutes=EXPECTED_PREPARATION_MINUTES
    )


def create_order_record(request: OrderRequest, invoice: InvoiceResponse):
    global ORDER_COUNTER

    with ORDER_LOCK:
        ORDER_COUNTER += 1
        order_id = f"ORD{ORDER_COUNTER}"

        order_record = {
            "order_id": order_id,
            "employee_id": request.employee_id,
            "employee_name": request.employee_name,
            "items": [item.model_dump() for item in invoice.items],
            "invoice": invoice.model_copy(update={"order_id": order_id}),
            "status": "Order Placed",
            "created_at": datetime.now(timezone.utc)
        }

        ORDERS[order_id] = order_record

    return order_record


def get_order(order_id: str):
    return ORDERS.get(order_id)


def create_order_response(order_record):
    return OrderResponse(
        order_id=order_record["order_id"],
        invoice=order_record["invoice"],
        created_at=order_record["created_at"]
    )


def get_elapsed_minutes(order_record, simulated_elapsed_minutes=None):
    if simulated_elapsed_minutes is not None:
        if simulated_elapsed_minutes < 0:
            raise ValueError("Elapsed minutes cannot be negative.")
        return simulated_elapsed_minutes

    elapsed_seconds = (
        datetime.now(timezone.utc) - order_record["created_at"]
    ).total_seconds()

    return max(0, int(elapsed_seconds // 60))


def update_order_status(order_id: str, status: str):
    order_record = ORDERS.get(order_id)

    if order_record:
        order_record["status"] = status

    return order_record
