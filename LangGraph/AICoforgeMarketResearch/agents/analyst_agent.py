"""
Responsibility: Read the Research Agent's output and perform SWOT analysis.
SWOT means:
S - Strengths
W - Weaknesses
O - Opportunities
T - Threats
"""

from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)
from services.llm_service import create_llm
from models.market_models import AnalysisResult
from graph.state import MarketState

def analyst_agent(state: MarketState):

    print("Market Analyst Agent Started")

    research = state.get("research_result")

    if research is None:
        raise ValueError(
            "Research must be completed before analysis."
        )

    llm = create_llm()

    structured_llm = llm.with_structured_output(
        AnalysisResult
    )

    system_prompt = """
    You are an Enterprise Business Market Analyst.

    Your responsibilities:

    - Analyze the supplied market research.
    - Identify company strengths.
    - Identify potential weaknesses.
    - Identify market opportunities.
    - Identify business threats.
    - Generate practical recommendations.

    Rules:

    - Base conclusions on the provided research.
    - Do not invent company-specific facts.
    - Mark unsupported assumptions as assumptions.
    - Return structured SWOT analysis.
    """

    user_prompt = f"""
    Company: {state['company']}
    Industry: {state['industry']}
    Country: {state['country']}

    Original Business Question:
    {state['question']}

    Research Findings:
    {research.model_dump_json(indent=2)}

    Perform SWOT analysis and generate business recommendations.
    """

    result = structured_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])

    print("Market Analyst Agent Completed")

    return {
        "analysis_result": result,
        "completed_agents": (
            state.get("completed_agents",[]) 
            + ["Market Analyst Agent"]
        )
    }    