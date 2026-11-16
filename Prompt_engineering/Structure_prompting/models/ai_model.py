from pydantic import BaseModel,Field

#Model 1: API Request
class LearnerRequest(BaseModel):

    LearnerName: str = Field(min_length = 1)
    department: str = Field(min_length = 1)
    pythonScore: int = Field(ge = 0,le = 100)
    sqlScore: int = Field(ge = 0,le = 100)
    fastapiScore: int = Field(ge = 0,le = 100)
    attendancePercentage: float = Field(ge = 0,le = 100)
    assignmentCompleted: int = Field(ge = 0)
    totalAssignment: int = Field(ge = 0)

#Model 2: AI Analysis
class LearnerAnalysis(BaseModel):

    averageScore: float
    performanceLevel: str
    strongestTechnology: str
    weakestTechnology: str
    technicalAssessment: str
    recommendedLearning: list[str]

#Model 3: Final API Response
class LearnerResponse(BaseModel):

    learnerName: str
    department: str
    analysis: LearnerAnalysis
    finalRecommendation: str        