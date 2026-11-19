from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config.azure_config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT
)
from models.order_model import EscalationAnswer
from prompts.escalation_prompt import SYSTEMPROMPT, HUMANPROMPT


def calculate_priority(elapsed_minutes: int):
    if elapsed_minutes <= 20:
        return "NORMAL", "No escalation"

    if elapsed_minutes <= 30:
        return "HIGH", "Cafeteria Supervisor"

    return "CRITICAL", "Cafeteria Manager"


def create_escalation_message(
    order_id: str,
    employee_id: str,
    employee_name: str,
    food_items: str,
    elapsed_minutes: int,
    delay_minutes: int,
    priority: str,
    recipient: str
):
    if not all([
        AZURE_OPENAI_ENDPOINT,
        AZURE_OPENAI_API_KEY,
        AZURE_OPENAI_API_VERSION,
        AZURE_OPENAI_DEPLOYMENT
    ]):
        raise ValueError(
            "Azure OpenAI configuration is missing. "
            "Please check the .env file before checking a delayed order."
        )

    llm = AzureChatOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_OPENAI_API_VERSION,
        temperature=0
    )

    structured_llm = llm.with_structured_output(EscalationAnswer)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEMPROMPT),
            ("human", HUMANPROMPT)
        ]
    )

    chain = prompt | structured_llm

    result = chain.invoke({
        "order_id": order_id,
        "employee_id": employee_id,
        "employee_name": employee_name,
        "food_items": food_items,
        "elapsed_minutes": elapsed_minutes,
        "delay_minutes": delay_minutes,
        "priority": priority,
        "recipient": recipient
    })

    # Python remains the source of truth for priority and recipient.
    return EscalationAnswer(
        priority=priority,
        recipient=recipient,
        message=result.message
    )
