from openai import OpenAI
from config.settings import AZURE_OPENAI_ENDPOINT,AZURE_OPENAI_API_KEY,AZURE_OPENAI_DEPLOYMENT
from models.model_role_based import PythonAIRequest, PythonAIResponse
from prompts.prompt_role_based import SYSTEM_PROMPT,HUMAN_PROMPT
import json

#
#Step-1 create LLM client outside the function
#create llm client outside the function
llm = OpenAI(
    api_key = AZURE_OPENAI_API_KEY,
    base_url = f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1"
)

#Step-2 define the service function
def analyze_python_role_based(request: PythonAIRequest) -> PythonAIResponse:

    # prepare the human prompt
    user_prompt = HUMAN_PROMPT.format(

        learner_name = request.learner_name,
        question = request.question,
        experience_level = request.experience_level
    )

    #Step-3 invoke the LLM
    response = llm.responses.parse(
        model = AZURE_OPENAI_DEPLOYMENT,
        instructions = SYSTEM_PROMPT,
        input = user_prompt,
        text_format = PythonAIResponse
    )

    #Step-4 extract the generated response
    ai_responses = response.output_text
    parse_data = json.loads(ai_responses)

    #Step-5 return 
    return PythonAIResponse(
        **parse_data
    )
