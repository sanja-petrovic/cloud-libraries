from fastapi import FastAPI, HTTPException, Depends
from database import SessionLocal, engine, Base
from models import RegisterData
from user import (
    register_user,
    can_borrow,
    increase_active_loans,
    decrease_active_loans,
    get_user_by_government_id,
)
from user import exists
from sqlalchemy.orm import Session
from uuid import UUID
import os

root_path = os.environ.get("ROOT_PATH", None)
app = FastAPI(openapi_prefix=f"/{root_path}") if root_path else FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user", status_code=201)
async def register_user_route(data: RegisterData, db: Session = Depends(get_db)):
    if exists(db, data.government_id):
        raise HTTPException(status_code=409, detail="User already exists.")
    register_user(db, data)
    return {"message": "Successfully registered new user"}


@app.get("/user/{id}/check", status_code=200)
async def check_user_route(id: UUID, db: Session = Depends(get_db)):
    allowed = can_borrow(db, id)
    return {"allowed": allowed}


@app.get("/user/{gov_id}", status_code=200)
async def get_by_gov_id(gov_id: str, db: Session = Depends(get_db)):
    user = get_user_by_government_id(db, gov_id)
    if user:
        return user.__dict__
    raise HTTPException(status_code=404, detail="User not found.")


@app.put("/user/{id}/borrow", status_code=200)
async def user_borrow_route(id: UUID, db: Session = Depends(get_db)):
    increase_active_loans(db, id)
    return {"message": "Successfully updated user"}


@app.put("/user/{id}/return", status_code=200)
async def user_borrow_route(id: UUID, db: Session = Depends(get_db)):
    decrease_active_loans(db, id)
    return {"message": "Successfully updated user"}
