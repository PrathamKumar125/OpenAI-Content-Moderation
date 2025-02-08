from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ModerationResult(Base):
    __tablename__ = "moderation_results"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    result = Column(String)