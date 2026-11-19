from fastapi import APIRouter, HTTPException, Query

from models.order_model import (
    OrderRequest,
    OrderResponse,
    DelayCheckResponse
)
from graphs.cafeteria_graph import workflow_graph
from services.order_service import (
    MENU,
    get_order,
    create_order_response,
    get_elapsed_minutes
)

router = APIRouter()


@router.get("/menu")
def get_menu():
    return {
        "menu": MENU
    }


@router.post("/order", response_model=OrderResponse, status_code=201)
def place_order(request: OrderRequest):

    try:
        result = workflow_graph.invoke({
            "request": request,
            "simulated_elapsed_minutes": 0
        })

        return create_order_response(result["order_record"])

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get("/order/{order_id}")
def check_order(order_id: str):

    order_record = get_order(order_id)

    if not order_record:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "order_id": order_record["order_id"],
        "employee_id": order_record["employee_id"],
        "employee_name": order_record["employee_name"],
        "items": order_record["items"],
        "invoice": order_record["invoice"],
        "status": order_record["status"],
        "created_at": order_record["created_at"]
    }


@router.post(
    "/order/{order_id}/check-delay",
    response_model=DelayCheckResponse
)
def check_order_delay(
    order_id: str,
    simulated_elapsed_minutes: int | None = Query(
        default=None,
        ge=0,
        description=(
            "Optional test value. If omitted, elapsed time is calculated "
            "from the saved order creation timestamp."
        )
    )
):

    order_record = get_order(order_id)

    if not order_record:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    elapsed_minutes = get_elapsed_minutes(
        order_record,
        simulated_elapsed_minutes
    )

    request = OrderRequest(
        employee_id=order_record["employee_id"],
        employee_name=order_record["employee_name"],
        items=[
            {
                "food_name": item["food_name"],
                "quantity": item["quantity"]
            }
            for item in order_record["items"]
        ]
    )

    try:
        result = workflow_graph.invoke({
            "request": request,
            "existing_order_record": order_record,
            "simulated_elapsed_minutes": elapsed_minutes
        })

        priority = result["priority"]
        delay_minutes = result["delay_minutes"]

        if priority == "NORMAL":
            escalated_to = "No escalation"
            message = (
                f'Order {order_id} is within the expected '
                f'{result["expected_minutes"]}-minute preparation time.'
            )
        else:
            escalation = result["escalation"]
            escalated_to = escalation.recipient
            message = escalation.message

        return DelayCheckResponse(
            order_id=order_id,
            employee_id=order_record["employee_id"],
            elapsed_minutes=elapsed_minutes,
            expected_minutes=result["expected_minutes"],
            delay_minutes=delay_minutes,
            priority=priority,
            escalated_to=escalated_to,
            message=message
        )

    except ValueError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
