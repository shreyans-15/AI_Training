from crewai import Agent
from config.settings import llm

editor = Agent(
    role="Research Topic Editor",
    goal="Read and edit the information recieved from a editor point of view",
    backstory=(
        "You are a experienced editor for research. You suggest practical, "
        "logical addition and deletion from the information recieved."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)
