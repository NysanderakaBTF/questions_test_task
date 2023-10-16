from sqlalchemy import BigInteger, Column, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP

from core.db.db_config import Base


class Question(Base):
    __tablename__ = 'questions'
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    text = Column(Text)
    answer = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True))
