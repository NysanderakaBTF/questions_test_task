from fastapi import FastAPI

from api.questions.question_api import question_router

app = FastAPI(
    title="Questions API",
    description="Questions API",
    version="0.0.1",
)

app.include_router(question_router)
