from crewai import Crew, Process
from agents.agents import (
    idea_generator,
    activity_planner,
    invitation_writer,
    quality_checker
)
from tasks.tasks import (
    create_event_idea_task,
    create_activity_task,
    create_invitation_task,
    create_quality_check_task
)


def main():

    print("==============================")
    print("        AI EVENT PLANNER")
    print("        Powered by CrewAI")
    print("==============================")

    event_name = input("Enter event name: ").strip()
    event_date = input("Enter event date: ").strip()
    target_audience = input("Enter target audience: ").strip()

    if not event_name or not event_date or not target_audience:
        print("Please provide the event name, date and target audience.")
        return

    # Step 1: Create the tasks in sequential order
    event_idea_task = create_event_idea_task(
        event_name,
        event_date,
        target_audience
    )
    activity_task = create_activity_task(event_idea_task)
    invitation_task = create_invitation_task(
        event_idea_task,
        activity_task
    )
    quality_check_task = create_quality_check_task(
        event_idea_task,
        activity_task,
        invitation_task
    )

    # Step 2: Create the crew with exactly four agents and tasks
    event_crew = Crew(
        agents=[
            idea_generator,
            activity_planner,
            invitation_writer,
            quality_checker
        ],
        tasks=[
            event_idea_task,
            activity_task,
            invitation_task,
            quality_check_task
        ],
        process=Process.sequential,
        verbose=True
    )

    # Step 3: Execute the crew
    try:
        event_crew.kickoff()

        print("\n========== PART A: EVENT IDEA ==========\n")
        print(event_idea_task.output.raw)

        print("\n========== PART B: FOUR ACTIVITIES ==========\n")
        print(activity_task.output.raw)

        print("\n========== PART C: INVITATION ==========\n")
        print(invitation_task.output.raw)

        print("\n========== PART D: FINAL CHECKLIST ==========\n")
        print(quality_check_task.output.raw)

    except Exception as error:
        print(
            "Unable to generate the event plan:",
            type(error).__name__,
            str(error)
        )


if __name__ == "__main__":
    main()
