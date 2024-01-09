from uuid import UUID, uuid4
from database import Base
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class Book(Base):
    __tablename__ = "books"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String)
    author = Column(String)
    isbn = Column(String, unique=True, index=True)


class Loan(Base):
    __tablename__ = "loans"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"))
    user_id = Column(UUID(as_uuid=True))
    date = Column(DateTime, default=datetime.now())
    returned = Column(DateTime, default=None)
