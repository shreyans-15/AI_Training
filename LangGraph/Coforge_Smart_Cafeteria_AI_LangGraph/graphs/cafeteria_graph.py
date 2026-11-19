from typing import TypedDict, Literal

from langgraph.graph import StateGraph, START, END

from models.order_model import OrderRequest, EscalationAnswer
from services.order_service import (
    validate_order,
    generate_invoice,
    create_order_record,
    get_elapsed_minutes,
    update_order_status
)
from services.escalation_service import (
    calculate_priority,
    create_escalation_message
)


class CafeteriaState(TypedDict, total=False):

    request: OrderRequest
    order_id: str
    employee_id: str
    employee_name: str
    validated_items: list
    invoice: object
    order_record: dict
    existing_order_record: dict
    elapsed_minutes: int
    expected_minutes: int
    delay_minutes: int
    priority: str
    recipient: str
    escalation: EscalationAnswer
    status: str
    simulated_elapsed_minutes: int


def validate_order_node(state: CafeteriaState):

    request = state["request"]
    validated_items = validate_order(request)

    return {
        "employee_id": request.employee_id,
        "employee_name": request.employee_name,
        "validated_items": validated_items
    }


def generate_invoice_node(state: CafeteriaState):

    # Reuse an existing order during a delay check.
    existing_order_record = state.get("existing_order_record")

    if existing_order_record:
        order_record = existing_order_record
    else:
        request = state["request"]
        invoice = generate_invoice(
            request,
            state["validated_items"]
        )
        order_record = create_order_record(request, invoice)

    return {
        "order_id": order_record["order_id"],
        "invoice": order_record["invoice"],
        "order_record": order_record,
        "status": order_record["status"],
        "expected_minutes": 20
    }


def check_delivery_node(state: CafeteriaState):

    order_record = state["order_record"]

    elapsed_minutes = get_elapsed_minutes(
        order_record,
        state.get("simulated_elapsed_minutes")
    )

    delay_minutes = max(
        0,
        elapsed_minutes - state["expected_minutes"]
    )

    priority, recipient = calculate_priority(elapsed_minutes)

    return {
        "elapsed_minutes": elapsed_minutes,
        "delay_minutes": delay_minutes,
        "priority": priority,
        "recipient": recipient
    }


def route_order(state: CafeteriaState) -> Literal["escalate_order", "confirm_order"]:

    if state["priority"] in ["HIGH", "CRITICAL"]:
        return "escalate_order"

    return "confirm_order"


def escalate_order_node(state: CafeteriaState):

    order_record = state["order_record"]

    food_items = ", ".join(
        f'{item["food_name"]} x {item["quantity"]}'
        for item in order_record["items"]
    )

    escalation = create_escalation_message(
        order_id=state["order_id"],
        employee_id=state["employee_id"],
        employee_name=state["employee_name"],
        food_items=food_items,
        elapsed_minutes=state["elapsed_minutes"],
        delay_minutes=state["delay_minutes"],
        priority=state["priority"],
        recipient=state["recipient"]
    )

    update_order_status(
        state["order_id"],
        f'Escalated - {state["priority"]}'
    )

    return {
        "escalation": escalation,
        "status": f'Escalated - {state["priority"]}'
    }


def confirm_order_node(state: CafeteriaState):

    update_order_status(state["order_id"], "Order Placed")

    return {
        "status": "Order Placed"
    }


# Create workflow
workflow = StateGraph(CafeteriaState)

# Add nodes
workflow.add_node("validate_order", validate_order_node)
workflow.add_node("generate_invoice", generate_invoice_node)
workflow.add_node("check_delivery", check_delivery_node)
workflow.add_node("escalate_order", escalate_order_node)
workflow.add_node("confirm_order", confirm_order_node)

# Add edges
workflow.add_edge(START, "validate_order")
workflow.add_edge("validate_order", "generate_invoice")
workflow.add_edge("generate_invoice", "check_delivery")

workflow.add_conditional_edges(
    "check_delivery",
    route_order,
    {
        "escalate_order": "escalate_order",
        "confirm_order": "confirm_order"
    }
)

workflow.add_edge("escalate_order", END)
workflow.add_edge("confirm_order", END)

workflow_graph = workflow.compile()
