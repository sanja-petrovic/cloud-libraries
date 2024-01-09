from pydantic import BaseModel


class RegisterData(BaseModel):
    first_name: str
    last_name: str
    home_address: str
    government_id: str
