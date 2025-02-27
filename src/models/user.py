# src\models\user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: Optional[str] = None
    email: EmailStr
    full_name: Optional[str] = None
    disabled: bool = False

class UserInDB(User):
    password: str