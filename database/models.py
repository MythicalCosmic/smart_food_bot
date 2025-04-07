from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    language = Column(String)
    last_name = Column(String, nullable=True)
    state = Column(String)
    username = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
