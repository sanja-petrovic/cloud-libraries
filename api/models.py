from pydantic import BaseModel
from datetime import date


class RegisterData(BaseModel):
    first_name: str
    last_name: str
    home_address: str
    government_id: str


class BookData(BaseModel):
    title: str
    author: str
    isbn: str


class BorrowData(BaseModel):
    title: str
    author: str
    isbn: str
    user_id: str
