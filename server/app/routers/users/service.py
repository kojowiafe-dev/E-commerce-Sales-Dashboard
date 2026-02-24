from fastapi import HTTPException, status
from sqlmodel import select
from ...routers.auth import schemas
from ...database.core import SessionDep
from ...models.model import User
from uuid import UUID



async def get_users(session: SessionDep):
    users = await session.execute(select(User))
    return users.scalars().all()



async def get_user_by_id(user_id: UUID, session: SessionDep):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user



async def update_user(user_id: UUID, user_update: schemas.UserBase, session: SessionDep):
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
        
        
    await session.commit()
    session.refresh(db_user)
    return db_user



async def delete_user(user_id: UUID, session: SessionDep):
    user = await session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    session.delete(user)
    await session.commit()