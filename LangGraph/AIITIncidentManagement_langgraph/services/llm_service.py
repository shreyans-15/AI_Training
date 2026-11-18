from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config.settings import (AZURE_OPENAI_ENDPOINT,AZURE_OPENAI_API_KEY,AZURE_OPENAI_API_VERSION,AZURE_OPENAI_DEPLOYMENT)
from models.incident_model import (IncidentRequest,IncidentAnalysis)
from prompts.incident_prompt import (SYSTEMPROMPT,HUMANPROMPT)

llm = AzureChatOpenAI(
   api_key= AZURE_OPENAI_API_KEY,
   azure_endpoint=AZURE_OPENAI_ENDPOINT,
   azure_deployment=AZURE_OPENAI_DEPLOYMENT,
   api_version=AZURE_OPENAI_API_VERSION,
   temperature=0
)

structured_llm = llm.with_structured_output(
    IncidentAnalysis
)

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

def analyze_incident(request:IncidentRequest) -> IncidentAnalysis:

    result = chain.invoke({
        "employee_id": request.employee_id,
        "employee_name": request.employee_name,
        "department": request.department,
        "issue": request.issue
    })

    return result
