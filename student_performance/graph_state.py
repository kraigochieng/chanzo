from enum import Enum
from typing import List

from langgraph.graph import MessagesState
from pydantic import BaseModel, Field


# Output Formats
class ClassificationEnum(Enum):
    grade_probability = "Grade Probability"
    strength_or_weakness = "Strength and weakness of student"
    career_recommendations = "Career recommendation for student"
    other = "other"


class Classification(BaseModel):
    classification: ClassificationEnum = Field("Classificaton of the query")


class Recommendation(BaseModel):
    stream: str = Field(description="The class the student is in")
    name: str = Field(description="The student's name")
    subject: str = Field(description="The subject")
    subject_strand: str = Field(description="The specific topic within the subject")
    grade_numeric: float = Field(description="The grade bound between 1 and 5")
    percentile: float = Field(description="Percentile of student")
    strength_or_weakness: str = Field(
        description="Describe if the student is strong or weak relative to class, use percentile"
    )
    recommendations: str = Field(
        description="A generic recommendation on what they should do. Maybe focus on another strand within the subject or focus on another subject altogether"
    )


class RecommendationList(BaseModel):
    recommendations: List[Recommendation]


# ## State
#


class State(MessagesState):
    summary: str
    # text: str
    # classification: ClassificationEnum
    # recommendations: List[Recommendation]