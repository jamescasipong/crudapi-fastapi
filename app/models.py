from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr, validator
from typing import Literal

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal['user', 'admin']

    def serialized(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
        }
