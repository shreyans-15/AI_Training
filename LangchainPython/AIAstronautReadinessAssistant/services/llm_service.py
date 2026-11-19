from config.settings import (AZURE_OPENAI_ENDPOINT,AZURE_OPENAI_API_KEY,AZURE_OPENAI_API_VERSION,AZURE_OPENAI_DEPLOYMENT)
from models.astronaut_model import (AstronautRequest,AstronautAnalysis,AstronautResponse)
from prompts.astronaut_prompt import (SYSTEMPROMPT,HUMANPROMPT)
from services.eligibility_service import (evaluate_eligibility,get_readiness_status,build_fallback_explanation)
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

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

#If credentials are missing the app must not crash, so chain stays None
try:
    llm = AzureChatOpenAI(
       api_key= AZURE_OPENAI_API_KEY,
       azure_endpoint=AZURE_OPENAI_ENDPOINT,
       azure_deployment=AZURE_OPENAI_DEPLOYMENT,
       api_version=AZURE_OPENAI_API_VERSION,
       temperature=0
    )

    structured_llm = llm.with_structured_output(
        AstronautResponse
    )

    chain = prompt | structured_llm

except Exception:
    chain = None


#Step1: build the prompt input from the request and the Python analysis
def build_chain_input(request:AstronautRequest,analysis:AstronautAnalysis):

    return {
        "astronaut_id" :request.astronaut_id,
        "astronaut_name":request.astronaut_name,
        "age":request.age,
        "training_hours":request.training_hours,
        "medical_clearance":request.medical_clearance,
        "previous_missions":request.previous_missions,
        "mission_type":request.mission_type,
        "age_eligible":analysis.age_eligible,
        "training_eligible":analysis.training_eligible,
        "medical_eligible":analysis.medical_eligible,
        "experience_eligible":analysis.experience_eligible,
        "failed_checks":", ".join(analysis.failed_checks) if analysis.failed_checks else "None",
        "risk_level":analysis.risk_level,
        "readiness_status":get_readiness_status(analysis)
    }

#Step2: build the final response - decision fields always come from Python
def build_response(request:AstronautRequest,analysis:AstronautAnalysis,llm_result)->AstronautResponse:

    reason = None
    recommendation = None

    if llm_result is not None:
        reason = llm_result.reason
        recommendation = llm_result.recommendation

    #use the deterministic explanation when the LLM gave nothing usable
    if not reason or not reason.strip() or not recommendation or not recommendation.strip():
        reason, recommendation = build_fallback_explanation(request,analysis)

    return AstronautResponse(
        astronaut_id = request.astronaut_id,
        astronaut_name = request.astronaut_name,
        mission_type = request.mission_type,
        readiness_status = get_readiness_status(analysis),
        risk_level = analysis.risk_level,
        reason = reason,
        recommendation = recommendation
    )

#NORMAL CHAIN : one astronaut -> chain.invoke
def analyze_astronaut(request:AstronautRequest)->AstronautResponse:

    analysis = evaluate_eligibility(request)

    llm_result = None

    if chain is not None:
        try:
            llm_result = chain.invoke(
                build_chain_input(request,analysis)
            )
        except Exception:
            llm_result = None

    return build_response(request,analysis,llm_result)

#BATCH PROCESSING : many astronauts -> chain.batch
def analyze_astronauts(requests:list[AstronautRequest])->list[AstronautResponse]:

    analyses = [evaluate_eligibility(request) for request in requests]

    if chain is not None:
        batch_inputs = [
            build_chain_input(request,analysis)
            for request,analysis in zip(requests,analyses)
        ]

        #return_exceptions=True : one failed call does not stop the whole batch
        results = chain.batch(
            batch_inputs,
            config={"max_concurrency":5},
            return_exceptions=True
        )
    else:
        results = [None] * len(requests)

    responses = []

    for request,analysis,result in zip(requests,analyses,results):

        if isinstance(result,Exception):
            result = None

        responses.append(build_response(request,analysis,result))

    return responses
