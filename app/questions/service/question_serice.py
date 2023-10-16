from typing import List

import aiohttp
from fastapi import HTTPException
from sqlalchemy import select

from app.questions.models.question import Question
from app.questions.schema.qestion import QuestionSchema
from core.db.db_config import provide_session


class QuestionService:

    @classmethod
    async def save_questions_batch(cls, question: List[QuestionSchema]) -> List[Question]:
        async with provide_session() as session:
            questions_objects = [Question(**i.dict()) for i in question]
            session.add_all(questions_objects)
            await session.commit()
            return questions_objects

    @classmethod
    async def get_questions(cls, number_of_questions: int) -> List[Question]:
        inserted_questions = []

        while number_of_questions > 0:
            async with aiohttp.ClientSession() as session:
                try:
                    resp = await session.get(f'https://jservice.io/api/random?count={number_of_questions}')
                    resp = await resp.json()
                except Exception as e:
                    raise HTTPException(status_code=424, detail="External service error")

                resp1 = list({i['id']: i for i in resp}.values())
                question_ids = [i['id'] for i in resp1]

                async with provide_session() as db:
                    presented_questions = await db.execute(select(Question.id)
                                                           .where(Question.id.in_(question_ids)))

                    presented_question_ids = presented_questions.scalars().all()

                    questions_to_save = [QuestionSchema(id=i['id'],
                                                        answer=i['answer'],
                                                        text=i['question'],
                                                        created_at=i['created_at'])
                                         for i in resp1 if i['id'] not in presented_question_ids]
                    saved_q = await cls.save_questions_batch(questions_to_save)
                    inserted_questions.extend(saved_q)
                    number_of_questions -= len(saved_q)
        return inserted_questions
