from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str  # A senha será armazenada como hash no banco
