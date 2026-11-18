from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from services.llm_service import analyze_incident
from models.incident_model import (
    IncidentRequest,
    IncidentAnalysis
)

# creating the state

class IncidentState(TypedDict):
    employee_id: str
    employee_name: str
    department: str
    issue: str

    category: str
    priority: str
    summary: str
    business_impact: str
    suggested_resolution: str
    escalation_required: bool
    email_sent: bool
    email_message: str
    status: str


# Node 1 : LangChain call (AI analysis)
def analyze_incident_node(
        state: IncidentState
):

    request = IncidentRequest(
        employee_id=state["employee_id"],
        employee_name=state["employee_name"],
        department=state["department"],
        issue=state["issue"]
    )

    result = analyze_incident(request)

    return {
        "category": result.category,
        "priority": result.priority,
        "summary": result.summary,
        "business_impact": result.business_impact,
        "suggested_resolution": result.suggested_resolution
    }


# Conditional router : decides the next node using priority
def check_incident_priority(
        state: IncidentState
):
    if state["priority"] in ["Critical", "High"]:
        return "Escalate"

    return "Resolve"


# Node 2 : Critical / High -> escalate (email is only simulated)
def escalate_incident_node(state: IncidentState):
    return {
        "escalation_required": True,
        "email_sent": True,
        "email_message": "Email sent to IT support team",
        "status": "Escalated"
    }


# Node 3 : Medium / Low -> only give the suggested resolution
def provide_resolution_node(
        state: IncidentState
):
    return {
        "escalation_required": False,
        "email_sent": False,
        "email_message": "Email not required",
        "status": "Resolution Provided"
    }


# Create Workflow

workflow = StateGraph(
    IncidentState
)


# Add Nodes

workflow.add_node(
    "analyze_incident_node",
    analyze_incident_node)

workflow.add_node("escalate_incident_node", escalate_incident_node)
workflow.add_node("provide_resolution_node", provide_resolution_node)

# Starting Edge

workflow.add_edge(START, "analyze_incident_node")

workflow.add_conditional_edges(
    "analyze_incident_node",
    check_incident_priority,
    {
        "Escalate": "escalate_incident_node",
        "Resolve": "provide_resolution_node"
    }
)

workflow.add_edge("escalate_incident_node", END)

workflow.add_edge("provide_resolution_node", END)


workflow_graph = workflow.compile()
