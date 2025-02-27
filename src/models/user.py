# src\models\user.py
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    password: str
    disabled: bool | None = True

class UserInDB(User):
    hashed_password: str