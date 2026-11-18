from crewai import Agent
from config.settings import llm
 
assessment_agent = Agent(

    role = "Python Assessment Specialist",
    goal = (
        "Create practical Python assessments"
        "Based on the concepts taught by"
        "the python Tutor"
    ),
    backstory= (
        "You are an experienced Python assessment"
        "designer. You prepare coding assignments"
        "for freshers and evaluate their"
        "problem-solving understanding."
    ),

    llm = llm,
    verbose = True,
    allow_delegation = False
)