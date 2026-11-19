# Coforge Smart Cafeteria AI

Food ordering, invoice generation and delay escalation using FastAPI,
LangChain, Azure OpenAI and LangGraph.

## Features

- Fixed cafeteria menu stored in `config/menu.json`.
- Pydantic validation for employee and food-order details.
- In-memory order storage with unique order and invoice numbers.
- Invoice calculation with 5% GST.
- LangGraph workflow with validation, invoice, delivery-check,
  escalation and confirmation nodes.
- Python-controlled priority calculation:
  - 0-20 minutes: NORMAL
  - 21-30 minutes: HIGH - Cafeteria Supervisor
  - More than 30 minutes: CRITICAL - Cafeteria Manager
- LangChain structured output for professional escalation messages.
  The priority and recipient in the final API response always come
  from Python, not from the LLM.

No database is required. Orders are stored in memory and are lost when
the application stops.

## Setup

```bash
python -m venv venv
pip install -r requirements.txt
```

Activate the virtual environment, copy `.env.example` to `.env`, and
fill in your Azure OpenAI settings.

Run the API from this project folder:

```bash
uvicorn main:app --reload
```

Open the FastAPI Swagger page at `http://127.0.0.1:8000/docs`.

## Endpoints

- `GET /menu`
- `POST /order`
- `GET /order/{order_id}`
- `POST /order/{order_id}/check-delay`
- `GET /health`

## Sample order request

```json
{
  "employee_id": "EMP101",
  "employee_name": "Rahul Sharma",
  "items": [
    {"food_name": "Veg Sandwich", "quantity": 2},
    {"food_name": "Coffee", "quantity": 1}
  ]
}
```

Expected invoice: subtotal ₹200.00, GST ₹10.00 and total payable ₹210.00.

## Testing delay escalation

By default, the delay endpoint calculates elapsed minutes from the saved
order creation timestamp. For testing, pass the optional query parameter:

`POST /order/ORD1001/check-delay?simulated_elapsed_minutes=26`

Use 26 to test HIGH priority and 38 to test CRITICAL priority.
The delayed-order path calls Azure OpenAI, so valid Azure configuration
is required for those paths.
