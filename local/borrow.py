from sqlalchemy.orm import Session
from schemas import Loan
from models import LoanData, BookData
from uuid import UUID
from book import get_book_by_data
from datetime import datetime


def borrow(db: Session, data: LoanData) -> Loan:
    book_data = BookData(title=data.title, author=data.author, isbn=data.isbn)
    book = get_book_by_data(db, book_data)
    if book is None:
        return None
    loan = Loan(book_id=book.id, user_id=data.user_id)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    print(loan.__dict__)
    return loan


def return_book(db: Session, loan_id: UUID) -> Loan:
    query = db.query(Loan).filter(Loan.id == loan_id, Loan.returned == None)
    if not query.first():
        return None
    loan = query.first()
    query.update({"returned": datetime.now()})
    db.commit()
    return loan
