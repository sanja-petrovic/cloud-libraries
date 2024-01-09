from fastapi import FastAPI, status, HTTPException, Depends
from database import SessionLocal, engine, Base
from models import UserData
from user import exists, register_user
from sqlalchemy.orm import Session

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserData, db: Session = Depends(get_db)):
    if exists(db, user.government_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists."
        )
    register_user(db, user)
    return {"message": "Successfully registered new user"}
