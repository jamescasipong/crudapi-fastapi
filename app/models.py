from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

    def serialized(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
        }
    
    def list(self) -> list:
        return [self.serialized() for self in self] 