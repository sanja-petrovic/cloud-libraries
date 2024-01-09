from sqlalchemy.orm import Session
from schemas import User
from models import RegisterData
from uuid import UUID


def register_user(db: Session, user: RegisterData):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        home_address=user.home_address,
        government_id=user.government_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_government_id(db: Session, government_id: str):
    return db.query(User).filter(User.government_id == government_id).first()


def exists(db: Session, government_id: str):
    return get_user_by_government_id(db, government_id) is not None
