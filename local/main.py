from fastapi import FastAPI, HTTPException, Depends
from database import SessionLocal, engine, Base
from models import BookData, LoanData, RegisterData
from book import add_book
from book import exists, get_book_by_isbn
from borrow import borrow, return_book, get_loans_by_user
from sqlalchemy.orm import Session
from uuid import UUID
import requests
import json
import os

app = FastAPI()
Base.metadata.create_all(bind=engine)

central_api = "http://central-library:8000"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/book", status_code=201)
async def add_book_route(data: BookData, db: Session = Depends(get_db)):
    if exists(db, data.isbn):
        raise HTTPException(status_code=409, detail="Book already exists.")
    add_book(db, data)
    return {"message": "Successfully added a new book"}


@app.post("/user", status_code=201)
async def register_user_route(data: RegisterData):
    return requests.post(
        url=f"{central_api}/user", json=data.model_dump(mode="json"), timeout=5
    ).json()


@app.post("/borrow", status_code=200)
async def borrow_book_route(data: LoanData, db: Session = Depends(get_db)):
    if can_borrow(data.user_id):
        borrowed = borrow(db, data)
        if borrowed is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        requests.put(url=f"{central_api}/user/{borrowed.user_id}/borrow", timeout=5)
        return {
            "message": f"User {data.user_id} successfully borrowed book {data.title} by {data.author}"
        }
    raise HTTPException(status_code=403, detail="User has too many active loans.")


def can_borrow(user_id: UUID):
    response = requests.get(url=f"{central_api}/user/{user_id}/check", timeout=5).json()
    return response["allowed"]


@app.get("/book/{isbn}", status_code=200)
async def get_by_isbn(isbn: str, db: Session = Depends(get_db)):
    book = get_book_by_isbn(db, isbn)
    if book:
        return book.__dict__
    raise HTTPException(status_code=404, detail="Book not found.")


@app.put("/return/{id}", status_code=200)
async def return_book_route(id: UUID, db: Session = Depends(get_db)):
    loan = return_book(db, id)
    if loan:
        requests.put(url=f"{central_api}/user/{loan.user_id}/return", timeout=5)
        return {"message": "User successfully returned book."}
    return {
        "message": "User did not return book, possibly because it's been returned already."
    }


@app.get("/user/{id}/loans")
async def get_user_loans(id: UUID, db: Session = Depends(get_db)):
    loans = get_loans_by_user(db, id)
    print(loans)
    return loans
