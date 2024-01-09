from uuid import UUID, uuid4
from database import Base
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String)
    last_name = Column(String)
    home_address = Column(String)
    government_id = Column(String, unique=True, index=True)


class Book(Base):
    __tablename__ = "books"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String)
    author = Column(String)
    isbn = Column(String, unique=True, index=True)


class Borrowing(Base):
    __tablename__ = "borrowings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.now())
    returned = Column(DateTime, default=None)
