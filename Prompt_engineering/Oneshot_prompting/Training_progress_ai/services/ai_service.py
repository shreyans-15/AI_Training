import json

from fastapi import HTTPException
from openai import AzureOpenAI, APIError, APITimeoutError, RateLimitError
from pydantic import ValidationError

from config.settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
)
from models.analysis_model import LearnerProgressAnalysis
from models.request_model import LearnerProgressRequest
from models.response_model import LearnerProgressResponse
from prompts.one_shot_prompt import HUMAN_PROMPT, SYSTEM_PROMPT

llm = None

if (
    AZURE_OPENAI_API_KEY
    and AZURE_OPENAI_API_VERSION
    and AZURE_OPENAI_DEPLOYMENT
    and AZURE_OPENAI_ENDPOINT
):
    llm = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_OPENAI_API_VERSION,
    )


def analyze_learner_progress(
    request: LearnerProgressRequest,
) -> LearnerProgressResponse:

    if llm is None:
        raise HTTPException(
            status_code=503,
            detail="Azure OpenAI is not configured.",
        )

    if request.assignments_assigned == 0:
        completion_percentage = 0.0
        insufficient_assignment_evidence = True

    else:

        completion_percentage = (
            request.assignments_completed / request.assignments_assigned
        ) * 100

        insufficient_assignment_evidence = False

    user_prompt = HUMAN_PROMPT.format(
        learner_id=request.learner_id,
        learner_name=request.learner_name,
        training_program=request.training_program,
        topics_completed=", ".join(request.topics_completed),
        assignments_assigned=request.assignments_assigned,
        assignments_completed=request.assignments_completed,
        completion_percentage=completion_percentage,
        insufficient_assignment_evidence=insufficient_assignment_evidence,
        attendance_percentage=request.attendance_percentage,
        coding_assessment_score=request.coding_assessment_score,
        trainer_feedback=request.trainer_feedback,
    )

    try:
        response = llm.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
    except (APITimeoutError, RateLimitError, APIError):
        raise HTTPException(
            status_code=502,
            detail="The AI service could not assess learner progress at this time.",
        )

    ai_text = response.choices[0].message.content

    if not ai_text:
        raise HTTPException(
            status_code=502,
            detail="The AI service returned an empty response.",
        )

    try:
        ai_data = json.loads(ai_text)
        ai_data["completion_percentage"] = completion_percentage
        ai_analysis = LearnerProgressAnalysis(**ai_data)
        
    except (json.JSONDecodeError, TypeError, ValueError, ValidationError):
        raise HTTPException(
            status_code=502,
            detail="The AI service returned an invalid learner progress analysis.",
        )

    recommended_practice = [
        f"Complete practical exercises and debugging tasks related to {topic}."
        for topic in ai_analysis.weak_topics
    ]

    if not recommended_practice:
        recommended_practice.append(
            "Continue practising completed topics with independent coding exercises."
        )

    next_learning_plan = (
        f"Focus first on {ai_analysis.improvement_priority}. "
        "Then complete practical exercises and review the results with the trainer."
    )

    if insufficient_assignment_evidence:
        trainer_recommendation = (
            "Collect assignment evidence before making a firm progress assessment. "
            f"Current advisory learning level: {ai_analysis.learning_level}."
        )
    else:
        trainer_recommendation = (
            "Review the learner's progress and provide guidance on "
            f"{ai_analysis.improvement_priority}"
        )

    ai_summary = (
        f"{request.learner_name} has completed {completion_percentage:.1f}% "
        f"of assigned work. The assessed learning level is "
        f"{ai_analysis.learning_level}, with an advisory readiness score of "
        f"{ai_analysis.readiness_score:.1f}/100. Main improvement priority: "
        f"{ai_analysis.improvement_priority}"
    )

    return LearnerProgressResponse(
        learner_id=request.learner_id,
        learner_name=request.learner_name,
        analysis=ai_analysis,
        recommended_practice=recommended_practice,
        next_learning_plan=next_learning_plan,
        trainer_recommendation=trainer_recommendation,
        ai_summary=ai_summary,
    )
