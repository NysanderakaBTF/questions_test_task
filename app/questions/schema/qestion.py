from datetime import datetime

from pydantic import BaseModel, Field


class QuestionSchema(BaseModel):
    id: int = Field(..., description="Id of the Question, got from request")
    text: str = Field(..., description="Text of the Question")
    answer: str = Field(..., description="Answer")
    created_at: datetime = Field(..., description="Date when question was created")

    class Config:
        orm_mode = True


class QuestionRequest(BaseModel):
    questions_num: int = Field(..., description="Number of questions to get")
