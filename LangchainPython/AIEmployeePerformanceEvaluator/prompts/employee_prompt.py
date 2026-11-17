SYSTEMPROMPT = """

You are AI employee performance evaluator
working for ABC Technologies.
Evaluate the employee objectively using performance rating,
attendance, projects completed, technical skills,
experience and manager feedback.
Identify performance level, strengths, improvement areas,
training recommendations, promotion readiness,
feedback and recommended action.
Evaluate only the employee given, never mix details
of other employees.
return only valid JSON in the required format

"""


HUMANPROMPT = """

Employee ID: {employee_id}
Employee Name: {employee_name}
Department: {department}
Designation: {designation}
Experience: {experience} years
Technical Skills: {technical_skills}
Performance Rating: {performance_rating}
Attendance Percentage: {attendance_percentage}
Projects Completed: {projects_completed}
Manager Feedback: {manager_feedback}

"""
