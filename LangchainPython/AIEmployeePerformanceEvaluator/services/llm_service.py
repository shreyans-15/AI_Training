from config.settings import (AZURE_OPENAI_ENDPOINT,AZURE_OPENAI_API_KEY,AZURE_OPENAI_API_VERSION,AZURE_OPENAI_DEPLOYMENT)
from models.employee_model import (
    
    BatchEmployeeRequest,
    BatchEmployeeResponse,
    EmployeeResponse
)
from prompts.employee_prompt import (SYSTEMPROMPT,HUMANPROMPT)
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = AzureChatOpenAI(

   api_key= AZURE_OPENAI_API_KEY,
   azure_endpoint=AZURE_OPENAI_ENDPOINT,
   azure_deployment=AZURE_OPENAI_DEPLOYMENT,
   api_version=AZURE_OPENAI_API_VERSION,
   temperature=0
)

structured_llm = llm.with_structured_output(
    EmployeeResponse
)

#Create the Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system" ,SYSTEMPROMPT
        ),
        (
            "human",HUMANPROMPT
        )


    ]
)

chain = prompt | structured_llm

def evaluate_employees(request:BatchEmployeeRequest)->BatchEmployeeResponse:

    #Step1: Build one input per employee
    batch_inputs = []

    for employee in request.employees:
        batch_inputs.append({
            "employee_id" :employee.employee_id,
            "employee_name":employee.employee_name,
            "department":employee.department,
            "designation":employee.designation,
            "experience":employee.experience,
            "technical_skills":", ".join(employee.technical_skills),
            "performance_rating":employee.performance_rating,
            "attendance_percentage":employee.attendance_percentage,
            "projects_completed":employee.projects_completed,
            "manager_feedback": employee.manager_feedback
        })

    #Step2: Batch processing - each employee gets an independent evaluation
    results = chain.batch(
        batch_inputs,
        config={"max_concurrency":5}
    )

    #Step3: Return the batch response
    return BatchEmployeeResponse(
        total_employees=len(results),
        results=results
    )
