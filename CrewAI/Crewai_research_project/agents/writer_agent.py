from crewai import Agent
from config.settings import llm

writer = Agent(
    role="Research Information Writer",
    goal="Edit the available information such that their are no grammatical and spelling mistakes.",
    backstory=(
        "You are a experienced research writer, "
        "make sure you write the desired and valuable information for the readers."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)