from typing import List

from fastapi import APIRouter

from app.questions.schema.qestion import QuestionSchema, QuestionRequest
from app.questions.service.question_serice import QuestionService

question_router = APIRouter(prefix="/questions",
                            tags=["questions"])


@question_router.post("/",
                      response_model=List[QuestionSchema],
                      description="Get a list of questions")
async def get_questions(quantity: QuestionRequest):
    return await QuestionService.get_questions(quantity.questions_num)
