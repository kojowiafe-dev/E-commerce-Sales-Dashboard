from sqlmodel import SQLModel
from uuid import UUID
from pydantic import EmailStr


class UserResponse(SQLModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str


class PasswordChange(SQLModel):
    current_password: str
    new_password: str
    new_password_confirm: str