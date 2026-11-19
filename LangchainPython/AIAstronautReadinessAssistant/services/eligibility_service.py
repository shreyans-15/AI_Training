from models.astronaut_model import (AstronautRequest,AstronautAnalysis)

#Step1: eligibility rules (plain Python, no LLM)
MIN_MISSION_AGE = 25
MAX_MISSION_AGE = 55
MIN_TRAINING_HOURS = 200

def evaluate_eligibility(request:AstronautRequest)->AstronautAnalysis:

    age_eligible = MIN_MISSION_AGE <= request.age <= MAX_MISSION_AGE
    training_eligible = request.training_hours >= MIN_TRAINING_HOURS
    medical_eligible = request.medical_clearance

    #only Exploration missions need a previous mission
    if request.mission_type == "Exploration":
        experience_eligible = request.previous_missions >= 1
    else:
        experience_eligible = True

    #Step2: collect the names of the failed checks
    failed_checks = []

    if not age_eligible:
        failed_checks.append("Age")

    if not training_eligible:
        failed_checks.append("Training")

    if not medical_eligible:
        failed_checks.append("Medical")

    if not experience_eligible:
        failed_checks.append("Experience")

    #Step3: risk level
    if not failed_checks:
        risk_level = "LOW"
    elif not medical_eligible:
        risk_level = "HIGH"
    else:
        risk_level = "MEDIUM"

    return AstronautAnalysis(
        age_eligible = age_eligible,
        training_eligible = training_eligible,
        medical_eligible = medical_eligible,
        experience_eligible = experience_eligible,
        failed_checks = failed_checks,
        risk_level = risk_level
    )

def get_readiness_status(analysis:AstronautAnalysis)->str:

    #READY only when every check passes
    if not analysis.failed_checks:
        return "READY"

    return "NOT_READY"

#Safe explanation used when the LLM is unavailable or fails
def build_fallback_explanation(request:AstronautRequest,analysis:AstronautAnalysis):

    if not analysis.failed_checks:
        return (
            f"All eligibility checks passed for the {request.mission_type} mission.",
            "Proceed to mission assignment."
        )

    actions = {
        "Age": "Age must be between 25 and 55 years for mission eligibility.",
        "Training": f"Complete at least {MIN_TRAINING_HOURS} training hours (currently {request.training_hours}).",
        "Medical": "Obtain medical clearance before applying again.",
        "Experience": "Complete at least one previous mission before an Exploration mission."
    }

    reason = "Failed checks: " + ", ".join(analysis.failed_checks) + "."

    recommendation = " ".join(actions[check] for check in analysis.failed_checks)

    return reason, recommendation
