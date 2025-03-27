from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

   # Database setup
Base = declarative_base()
engine = create_engine("sqlite:///memory.db")
SessionLocal = sessionmaker(bind=engine)

   # Define a table for storing conversations
class ConversationHistory(Base):
    __tablename__ = "conversation_history"
    user_id = Column(String, primary_key=True, index=True)
    memory = Column(Text)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()