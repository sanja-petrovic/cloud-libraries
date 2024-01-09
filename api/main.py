from fastapi import FastAPI, status, HTTPException, Depends
from database import SessionLocal, engine, Base
from models import RegisterData, BookData, BorrowData
from user import register_user
from user import exists as user_exists
from book import add_book
from book import exists as book_exists
from borrow import borrow, can_borrow, return_book
from sqlalchemy.orm import Session
from uuid import UUID

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user", status_code=201)
async def register_user_route(data: RegisterData, db: Session = Depends(get_db)):
    if user_exists(db, data.government_id):
        raise HTTPException(status_code=409, detail="User already exists.")
    register_user(db, data)
    return {"message": "Successfully registered new user"}


@app.post("/book", status_code=201)
async def add_book_route(data: BookData, db: Session = Depends(get_db)):
    if book_exists(db, data.isbn):
        raise HTTPException(status_code=409, detail="Book already exists.")
    add_book(db, data)
    return {"message": "Successfully added a new book"}


@app.post("/borrow", status_code=200)
async def borrow_book_route(data: BorrowData, db: Session = Depends(get_db)):
    if can_borrow(db, data.user_id):
        borrowed = borrow(db, data)
        if borrowed is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        return {
            "message": f"User {data.user_id} successfully borrowed book {data.title} by {data.author}"
        }
    raise HTTPException(status_code=403, detail="User has too many active borrowings.")


@app.put("/return/{id}", status_code=200)
async def return_book_route(id: UUID, db: Session = Depends(get_db)):
    return_book(db, id)
    return {"message": f"User successfully returned book."}
