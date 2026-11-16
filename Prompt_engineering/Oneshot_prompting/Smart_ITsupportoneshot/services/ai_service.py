import json
from openai import AzureOpenAI, APIError, APITimeoutError, RateLimitError
from fastapi import HTTPException
from config.settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
)
from models.analysis_model import ITSupportAnalysis
from models.request_model import ITSupportRequest
from models.response_model import ITSupportResponse
from prompts.one_shot_prompt import HUMAN_PROMPT, SYSTEM_PROMPT
 
llm = None

if (
    AZURE_OPENAI_API_KEY
    and AZURE_OPENAI_API_VERSION
    and AZURE_OPENAI_DEPLOYMENT
    and AZURE_OPENAI_ENDPOINT
):
    llm = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_OPENAI_API_VERSION,
    )

def analyze_ticket(request: ITSupportRequest) -> ITSupportResponse:

    if llm is None:

        raise HTTPException(
            status_code=503,
            detail="Azure OpenAI is not configured. Please check the .env file.",
        )

    user_prompt = HUMAN_PROMPT.format(
        
        ticket_id=request.ticket_id,
        employee_id=request.employee_id,
        employee_name=request.employee_name,
        department=request.department,
        issue_description=request.issue_description,
        affected_system=request.affected_system,
    )

    try:
        response = llm.chat.completions.create(

            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )

    except (APITimeoutError, RateLimitError, APIError):
        raise HTTPException (
            status_code=502,
            detail="The AI service could not process the ticket at this time.",
        )

    ai_text = response.choices[0].message.content

    if not ai_text:

        raise HTTPException(
            status_code=502,
            detail="The AI service returned an empty response.",
        )

    try:
        ai_data = json.loads(ai_text)
        ai_analysis = ITSupportAnalysis(**ai_data)

    except (json.JSONDecodeError, TypeError, ValueError):

        raise HTTPException(

            status_code=502,
            detail="The AI service returned an invalid ticket analysis.",
        )

    # Starter escalation rule; align this with the organization's support policy.
    escalation_required = (

        ai_analysis.priority_level.strip().lower() in ["high", "critical"]
        or ai_analysis.impact_level.strip().lower() == "organization"
    )

    recommended_actions = ai_analysis.troubleshooting_steps

    ai_summary = (
        f"This ticket is categorized as {ai_analysis.issue_category} with "
        f"{ai_analysis.priority_level} priority and {ai_analysis.impact_level} impact. "
        f"Possible cause: {ai_analysis.suspected_root_cause}"
    )

    return ITSupportResponse(
        
        ticket_id=request.ticket_id,
        ticket_status="Analyzed",
        analysis=ai_analysis,
        recommended_actions=recommended_actions,
        escalation_required=escalation_required,
        ai_summary=ai_summary,
    )
