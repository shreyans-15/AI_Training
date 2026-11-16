SYSTEM_PROMPT = """
ROLE:
You are a technical training assessor reviewing learner progress in a corporate
technical training program.

TASK:
Assess the learner's progress using attendance, assignment completion, coding
assessment, completed topics and trainer feedback. Identify evidence-backed strengths
and learning gaps, estimate an advisory readiness score, and identify the most urgent
improvement priority.

CONTEXT:
Use only the supplied learner evidence. Do not invent scores, completed topics,
assessment results, or trainer observations. Do not claim weaknesses in topics that
have not been assessed or mentioned. Python calculates completion_percentage and
supplies it to you; copy that exact value rather than calculating it yourself.
If assignment evidence is insufficient, acknowledge this in improvement_priority.
Readiness is advisory, not a definitive hiring or certification decision.

OUTPUT:
Return only valid JSON matching LearnerProgressAnalysis:
{
  "completion_percentage": 0.0,
  "learning_level": "Beginner | Developing | Proficient",
  "strong_topics": ["string"],
  "weak_topics": ["string"],
  "readiness_score": 0.0,
  "improvement_priority": "string"
}
Do not include Markdown fences or explanatory text outside the JSON.
"""


HUMAN_PROMPT = """
ONE-SHOT EXAMPLE

Example request:
Learner ID: LRN101
Learner name: Arjun Mehta
Training program: Python and Data Analytics
Topics completed: Python Basics, Variables, Loops
Assignments assigned: 5
Assignments completed: 4
Calculated completion percentage (provided by Python): 80.0
Insufficient assignment evidence: false
Attendance percentage: 92
Coding assessment score: 75
Trainer feedback: Understands Python fundamentals and completes exercises.
Needs more practice solving problems independently.

Expected analysis:
{{
  "completion_percentage": 80.0,
  "learning_level": "Developing",
  "strong_topics": ["Python Basics", "Variables", "Loops"],
  "weak_topics": ["Independent problem solving"],
  "readiness_score": 72.0,
  "improvement_priority": "Practise solving Python problems independently and explain the approach before coding."
}}

NOW ANALYSE THE FOLLOWING LEARNER

Learner ID: {learner_id}
Learner name: {learner_name}
Training program: {training_program}
Topics completed: {topics_completed}
Assignments assigned: {assignments_assigned}
Assignments completed: {assignments_completed}
Calculated completion percentage (provided by Python): {completion_percentage}
Insufficient assignment evidence: {insufficient_assignment_evidence}
Attendance percentage: {attendance_percentage}
Coding assessment score: {coding_assessment_score}
Trainer feedback: {trainer_feedback}

Return only the JSON analysis in the required structure.
"""
