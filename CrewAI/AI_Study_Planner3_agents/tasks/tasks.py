from crewai import Task
from agents.agents import topic_explainer, study_planner, quiz_creator


def create_topic_explanation_task(topic):
    explanation_task = Task(
        description=(
            f"Explain the Python topic: {topic}. Assume the learner is a complete "
            "beginner. Use simple English, explain the main idea, include exactly "
            "one small Python example, and briefly explain the example."
        ),
        expected_output=(
            "A beginner-friendly explanation of the selected Python topic, "
            "followed by one small Python example and a short explanation."
        ),
        agent=topic_explainer
    )
    return explanation_task


def create_study_plan_task(topic, explanation_task):
    study_plan_task = Task(
        description=(
            f"Create a three-day beginner study plan for {topic}. Use the "
            "explanation from the previous task. Include Day 1, Day 2 and Day 3. "
            "Give each day clear learning activities and a small practice goal. "
            "Keep the workload realistic for a beginner."
        ),
        expected_output=(
            "A structured three-day study plan with separate Day 1, Day 2 and "
            "Day 3 sections. Each day includes learning activities and a practice goal."
        ),
        agent=study_planner,
        context=[explanation_task]
    )
    return study_plan_task


def create_quiz_task(topic, study_plan_task):
    quiz_task = Task(
        description=(
            f"Prepare exactly five easy practice questions about {topic}. Base "
            "every question on the study plan from the previous task. Do not "
            "include answers, hints or solutions."
        ),
        expected_output=(
            "Exactly five numbered beginner-friendly practice questions. "
            "Do not include answers or solutions."
        ),
        agent=quiz_creator,
        context=[study_plan_task]
    )
    return quiz_task
