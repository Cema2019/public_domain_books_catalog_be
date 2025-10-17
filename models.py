from sqlalchemy import Column, Integer, String
from database import Base  

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    authors = Column(String(255), nullable=True)
    subjects = Column(String(1000), nullable=True)
