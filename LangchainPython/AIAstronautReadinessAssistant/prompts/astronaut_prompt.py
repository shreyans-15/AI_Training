SYSTEMPROMPT = """

You are AI astronaut mission readiness assistant
working for a space research organization.
Explain the mission readiness decision using only
the astronaut details and eligibility results given.
The eligibility results are already calculated by Python.
Never change the readiness status or the risk level
and never invent astronaut details.
reason must be a short explanation of the decision.
recommendation must be a specific next step
based on the failed checks.
If no check failed, recommend proceeding to mission assignment.
return only valid JSON in the required format

"""


HUMANPROMPT = """

Astronaut ID: {astronaut_id}
Astronaut Name: {astronaut_name}
Age: {age}
Training Hours: {training_hours}
Medical Clearance: {medical_clearance}
Previous Missions: {previous_missions}
Mission Type: {mission_type}

Age Eligible: {age_eligible}
Training Eligible: {training_eligible}
Medical Eligible: {medical_eligible}
Experience Eligible: {experience_eligible}
Failed Checks: {failed_checks}
Risk Level: {risk_level}
Readiness Status: {readiness_status}

"""
