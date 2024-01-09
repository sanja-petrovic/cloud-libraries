from sqlalchemy.orm import Session
from schemas import Book
from models import BookData


def add_book(db: Session, data: BookData) -> Book:
    book = Book(title=data.title, author=data.author, isbn=data.isbn)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book_by_isbn(db: Session, isbn: str) -> Book:
    return db.query(Book).filter(Book.isbn == isbn).first()


def get_book_by_data(db: Session, data: BookData) -> Book:
    return (
        db.query(Book)
        .filter(
            Book.title == data.title
            and Book.author == data.author
            and Book.isbn == data.isbn
        )
        .first()
    )


def exists(db: Session, isbn: str) -> bool:
    return get_book_by_isbn(db, isbn) is not None
