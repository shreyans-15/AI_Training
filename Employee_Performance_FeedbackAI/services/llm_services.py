import json
from openai import OpenAI
from config.settings import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT
)

from models.ai_model import (
    EmployeeFeedbackRequest,
    EmployeeFeedbackResponse
)
 
from prompts.ai_prompt import SYSTEM_PROMPT, HUMAN_PROMPT
 
 
# Step-1 create LLM client outside the function
llm = OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1"
)
 
 
# Step-2 define the service function
def analyze_employee_feedback(request: EmployeeFeedbackRequest):
 
    # prepare the human prompt
    user_prompt = HUMAN_PROMPT.format(
        employee_name=request.employee_name,
        reviewer_name=request.reviewer_name,
        project_name=request.project_name,
        performance_rating=request.performance_rating,
        feedback=request.feedback
    )
 
    # Step-3 invoke the LLM
    response = llm.responses.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        instructions=SYSTEM_PROMPT,
        input=user_prompt
    )
 
    # Step-4 extract the generated response
    ai_text = response.output_text
 
    # Step-5 convert JSON string into Python dictionary
    result = json.loads(ai_text)
 
    # Step-6 return structured response
    return EmployeeFeedbackResponse(
        **result
    )