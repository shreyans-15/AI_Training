from crewai import Task
from agents.editor_agent import editor
from agents.researcher_agent import researcher
from agents.writer_agent import writer


def create_researcher_task(research_topic):

    researcher_task = Task(
        description=(
            f"""
            Conduct detailed research on the topic: {research_topic}.

            Gather important information including:
            - Introduction to the topic
            - Key concepts and explanations
            - Benefits and advantages
            - Challenges and limitations
            - Real-world applications
            - Latest trends and developments

            Provide only relevant and valuable information.
            Avoid unnecessary details and repetition.
            """
        ),
        expected_output=(
            """
            A well-structured research document containing:
            - Topic overview
            - Key concepts
            - Benefits
            - Challenges
            - Applications
            - Current trends

            The information should be factual, clear, and easy to understand.
            """
        ),
        agent=researcher,
    )

    return researcher_task


def create_writer_task(researcher_task):

    writer_task = Task(
        description=(
            """
            Review the research information provided by the researcher.

            Improve the content by:
            - Correcting grammar and spelling mistakes
            - Improving sentence structure
            - Making the content more professional
            - Enhancing readability and flow
            - Removing redundant information

            Preserve all important facts and details.
            """
        ),
        expected_output=(
            """
            A professionally written and grammatically correct research article
            with improved readability, clarity, and structure.
            """
        ),
        agent=writer,
        context=[researcher_task]
    )

    return writer_task


def create_editor_task(researcher_task, writer_task):

    editor_task = Task(
        description=(
            """
            Review the final article produced by the writer.

            Act as a senior research editor and:
            - Verify logical flow of information
            - Suggest necessary additions
            - Remove unnecessary content
            - Ensure consistency and accuracy
            - Improve overall quality and presentation
            - Make the document ready for publication

            Provide the final polished version.
            """
        ),
        expected_output=(
            """
            A publication-ready research document that:
            - Is factually accurate
            - Has excellent readability
            - Contains logical structure
            - Contains only relevant information
            - Is free from grammatical and spelling errors
            """
        ),
        agent=editor,
        context=[researcher_task, writer_task]
    )

    return editor_task