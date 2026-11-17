import json

from fastapi import HTTPException
from openai import AzureOpenAI, APIError, APITimeoutError, RateLimitError

from config.settings import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT,
)

from models.ai_model import (
    LearnerRequest,
    LearnerAnalysis,
    LearnerResponse,
)

from prompts.ai_prompt import SYSTEM_PROMPT, HUMAN_PROMPT


def get_performance_level(average_score: float) -> str:
    if average_score >= 85:
        return "Excellent"
    elif average_score >= 70:
        return "Good"
    elif average_score >= 50:
        return "Needs Improvement"
    else:
        return "Critical Improvement Required"


def analyse_learner(learner: LearnerRequest) -> LearnerResponse:

    if not all(
        [
            AZURE_OPENAI_ENDPOINT,
            AZURE_OPENAI_API_VERSION,
            AZURE_OPENAI_API_KEY,
            AZURE_OPENAI_DEPLOYMENT,
        ]
    ):
        raise HTTPException(
            status_code=500,
            detail="Azure OpenAI configuration is missing. Check your .env file.",
        )

    scores = {
        "Python": learner.pythonScore,
        "SQL": learner.sqlScore,
        "FastAPI": learner.fastapiScore,
    }

    average_score = round(sum(scores.values()) / len(scores), 2)

    performance_level = get_performance_level(average_score)

    strongest_technology = max(scores, key=scores.get)
    weakest_technology = min(scores, key=scores.get)

    if learner.totalAssignments == 0:
        completion_percentage = 0.0
    else:
        completion_percentage = round(
            learner.assignmentsCompleted
            / learner.totalAssignments
            * 100,
            2,
        )

    user_prompt = HUMAN_PROMPT.format(
        LearnerName=learner.learnerName,
        department=learner.department,
        pythonScore=learner.pythonScore,
        sqlScore=learner.sqlScore,
        fastapiScore=learner.fastapiScore,
        attendancePercentage=learner.attendancePercentage,
        assignmentCompleted=learner.assignmentsCompleted,
        totalAssignment=learner.totalAssignments,
        completion=completion_percentage,
    )

    try:

        client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
        )

        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )

        ai_content = response.choices[0].message.content

        if not ai_content:
            raise HTTPException(
                status_code=502,
                detail="Azure OpenAI returned an empty response.",
            )

        ai_data = json.loads(ai_content)

        analysis = LearnerAnalysis(
            averageScore=average_score,
            performanceLevel=performance_level,
            strongestTechnology=strongest_technology,
            weakestTechnology=weakest_technology,
            technicalAssessment=" ".join(
                ai_data.get("technicalAssessment", [])
            ),
            recommendedLearning=[
                "Practice advanced SQL queries",
                "Build FastAPI mini projects",
                "Complete coding assignments regularly",
            ],
        )

        return LearnerResponse(
            learnerName=learner.learnerName,
            department=learner.department,
            analysis=analysis,
            finalRecommendation=ai_data.get(
                "finalRecommendation",
                "Continue improving technical skills through consistent practice.",
            ),
        )

    except HTTPException:
        raise

    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise HTTPException(
            status_code=502,
            detail=f"Invalid response received from Azure OpenAI: {error}",
        )

    except (APITimeoutError, RateLimitError, APIError) as error:
        raise HTTPException(
            status_code=502,
            detail=f"Azure OpenAI service error: {error}",
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {error}",
        )