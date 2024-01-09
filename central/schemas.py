from uuid import UUID, uuid4
from database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String)
    last_name = Column(String)
    home_address = Column(String)
    government_id = Column(String, unique=True, index=True)
    active_loans = Column(Integer, default=0)
