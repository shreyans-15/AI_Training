from crewai import Task
from agents.agents import (
    idea_generator,
    activity_planner,
    invitation_writer,
    quality_checker
)

def create_event_idea_task(event_name, event_date, target_audience):
    event_idea_task = Task(
        description=(
            f"Plan an event named {event_name} on {event_date} for "
            f"{target_audience}. Suggest exactly one simple event theme. "
            "Do not invent a venue. Since no venue was supplied, state "
            "that the venue is To be confirmed."
        ),
        expected_output=(
            "One clear event theme with a short explanation. Include the "
            "event name, date and audience. State 'Venue: To be confirmed'."
        ),
        agent=idea_generator
    )
    return event_idea_task


def create_activity_task(event_idea_task):
    activity_task = Task(
        description=(
            "Use the theme and details from the previous task. Create exactly "
            "four simple activities suitable for the target audience. Give "
            "each activity a name and a one-sentence description."
        ),
        expected_output=(
            "Exactly four numbered activities, each with a name and brief "
            "description. All activities must fit the event theme."
        ),
        agent=activity_planner,
        context=[event_idea_task]
    )
    return activity_task


def create_invitation_task(event_idea_task, activity_task):
    invitation_task = Task(
        description=(
            "Write a short and friendly invitation. Use the event name, date, "
            "target audience, theme and four activities from the previous "
            "tasks. Do not invent a venue. Include 'Venue: To be confirmed'."
        ),
        expected_output=(
            "A short invitation containing the event name, date, audience, "
            "theme, activities and venue status."
        ),
        agent=invitation_writer,
        context=[event_idea_task, activity_task]
    )
    return invitation_task


def create_quality_check_task(
    event_idea_task,
    activity_task,
    invitation_task
):
    quality_check_task = Task(
        description=(
            "Review the previous task outputs. Check whether the event theme, "
            "exactly four activities, event date and invitation are present. "
            "Also check venue information. Mark each item Available or Missing. "
            "If no venue was supplied, mark it as 'To be confirmed'. Do not "
            "invent missing details."
        ),
        expected_output=(
            "A final checklist showing the status of the event theme, four "
            "activities, date, invitation and venue. Clearly identify missing "
            "information and do not claim an unprovided venue is confirmed."
        ),
        agent=quality_checker,
        context=[event_idea_task, activity_task, invitation_task]
    )
    return quality_check_task
