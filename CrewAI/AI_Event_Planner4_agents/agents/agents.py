from crewai import Agent
from config.settings import llm

idea_generator = Agent(
    role="Event Idea Generator",
    goal="Suggest one simple event theme based on the event details provided.",
    backstory=(
        "You are a creative college event coordinator. You suggest practical, "
        "inclusive themes suitable for student audiences."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

activity_planner = Agent(
    role="Activity Planner",
    goal="Create exactly four suitable activities for the proposed event.",
    backstory=(
        "You are an experienced student event organizer. You design simple, "
        "engaging activities that fit the event theme and audience."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

invitation_writer = Agent(
    role="Invitation Writer",
    goal="Write a short, friendly invitation using the confirmed event details.",
    backstory=(
        "You are a college communications coordinator. You write warm, clear "
        "invitations and never invent missing event information."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

quality_checker = Agent(
    role="Event Plan Quality Checker",
    goal="Check whether the theme, activities, date and invitation are present.",
    backstory=(
        "You are a careful event quality reviewer. You verify earlier task "
        "outputs and clearly mark missing details."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)
