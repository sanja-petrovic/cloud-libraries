from pydantic import BaseModel


class RegisterData(BaseModel):
    first_name: str
    last_name: str
    home_address: str
    government_id: str


class BookData(BaseModel):
    title: str
    author: str
    isbn: str


class LoanData(BaseModel):
    title: str
    author: str
    isbn: str
    user_id: str
