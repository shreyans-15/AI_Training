from crewai import Crew, Process
from agents.agents import topic_explainer, study_planner, quiz_creator
from tasks.tasks import (
    create_topic_explanation_task,
    create_study_plan_task,
    create_quiz_task
)


def main():

    print("==============================")
    print("       AI STUDY PLANNER")
    print("       Powered by CrewAI")
    print("==============================")

    topic = input("Enter Python topic: ").strip()

    if not topic:
        print("Please enter a valid Python topic.")
        return

    # Step 1: Create the tasks in sequential order
    explanation_task = create_topic_explanation_task(topic)
    study_plan_task = create_study_plan_task(topic, explanation_task)
    quiz_task = create_quiz_task(topic, study_plan_task)

    # Step 2: Create the crew with exactly three agents and tasks
    study_crew = Crew(
        agents=[topic_explainer, study_planner, quiz_creator],
        tasks=[explanation_task, study_plan_task, quiz_task],
        process=Process.sequential,
        verbose=True
    )

    # Step 3: Execute the crew
    try:
        study_crew.kickoff()

        print("\n========== PART A: TOPIC EXPLANATION ==========\n")
        print(explanation_task.output.raw)

        print("\n========== PART B: THREE-DAY STUDY PLAN ==========\n")
        print(study_plan_task.output.raw)

        print("\n========== PART C: FIVE PRACTICE QUESTIONS ==========\n")
        print(quiz_task.output.raw)

    except Exception as error:
        print(
            "Unable to generate the study plan:",
            type(error).__name__,
            str(error)
        )


if __name__ == "__main__":
    main()
