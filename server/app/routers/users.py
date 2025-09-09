from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from schemas import UserBase, UserLogin, UserRegister
from database import SessionDep
from models.model import User
from hashing import get_password_hash
from datetime import datetime
from uuid import UUID


router = APIRouter(
    prefix="/users", 
    tags=["Users"]
)


@router.get("/", response_model=list[UserBase])
def get_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users



@router.get("/{user_id}", response_model=UserBase)
def get_user_by_id(user_id: UUID, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user



@router.put("/{user_id}", response_model=UserBase)
def update_user(user_id: UUID, user_update: UserBase, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
        
        
    session.commit()
    session.refresh(db_user)
    return db_user



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    session.delete(user)
    session.commit()