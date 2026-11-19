from crewai import Crew, Process
from agents.editor_agent import editor
from agents.researcher_agent import researcher
from agents.writer_agent import writer
from tasks.researcher_tasks import (
    create_researcher_task,
    create_writer_task,
    create_editor_task
)


def main():

    print("==============================")
    print("        AI RESEARCHER")
    print("        Powered by CrewAI")
    print("==============================")

    rtopic = input("Enter research topic: ").strip()

    if not rtopic:
        print("Please provide the research topic name.")
        return

    # Step 1: Create the tasks in sequential order
    temp1 = create_researcher_task(rtopic)
    temp2 = create_writer_task(temp1)
    temp3 = create_editor_task(temp1,temp2)
        

    # Step 2: Create the crew with exactly four agents and tasks
    research_crew = Crew(
        agents=[
            editor,
            writer,
            researcher
        ],
        tasks=[
            temp1,
            temp2,
            temp3
        ],
        process=Process.sequential,
        verbose=True
    )

    # Step 3: Execute the crew
    try:
        research_crew.kickoff()

        print("\n========== PART A: RESEARCH TOPIC ==========\n")
        print(temp1.output.raw)

        print("\n========== PART B: WRITER TASK ==========\n")
        print(temp2.output.raw)

        print("\n========== PART C: EDITOR TASK ==========\n")
        print(temp3.output.raw)


    except Exception as error:
        print(
            "Unable to generate the research topic:",
            type(error).__name__,
            str(error)
        )


if __name__ == "__main__":
    main()
