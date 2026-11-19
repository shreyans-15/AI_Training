from crewai import Agent
from config.settings import llm
researcher = Agent(
    role="Research Topic Generator",
    goal="Based on the topic provided, provide the desired information to start and complete the research. Don't provide unnecessary information",
    backstory=(
        "You are an experienced researcher. You suggest practical, "
        "valuable information needed for the research topic."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)