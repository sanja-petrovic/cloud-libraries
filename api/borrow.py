from sqlalchemy.orm import Session
from schemas import Book, Borrowing
from models import BorrowData, BookData
from uuid import UUID
from book import get_book_by_data
from sqlalchemy import func
from sqlalchemy.sql.expression import false
from datetime import datetime


def borrow(db: Session, data: BorrowData) -> Borrowing:
    book_data = BookData(title=data.title, author=data.author, isbn=data.isbn)
    book = get_book_by_data(db, book_data)
    if book is None:
        return None
    borrowing = Borrowing(book_id=book.id, user_id=data.user_id)
    db.add(borrowing)
    db.commit()
    db.refresh(borrowing)
    print(get_active_borrowings_by_user(db, data.user_id))
    return borrowing


def get_active_borrowings_by_user(db: Session, user_id: UUID) -> int:
    return (
        db.query(Borrowing)
        .filter(Borrowing.user_id == user_id, Borrowing.returned == None)
        .count()
    )


def can_borrow(db: Session, user_id: UUID) -> bool:
    return get_active_borrowings_by_user(db, user_id) < 3


def return_book(db: Session, borrowing_id: UUID) -> None:
    old_borrowing = db.query(Borrowing).filter(Borrowing.id == borrowing_id)
    if not old_borrowing.first():
        return
    old_borrowing.update({"returned": datetime.now()})
    db.commit()
