from sqlmodel import SQLModel, Field
from datetime import datetime, date
from typing import Optional, List
from uuid import uuid4
from pydantic import EmailStr
from models.model import RoleEnum

    
    
class UserBase(SQLModel): 
    name: str
    email: Optional[str]
    role: RoleEnum

class UserRegister(UserBase):
    password: str

class UserLogin(SQLModel):
    name: str
    password: str
    role: str
    
    
class TokenData(SQLModel):
    username: Optional[str] = None
    
    def get_username(self) -> str | None:
        if self.username:
            return self.username
        return None


class Token(SQLModel):
    access_token: str
    token_type: str
    role: str