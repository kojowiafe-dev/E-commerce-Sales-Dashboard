from fastapi import APIRouter, status
from routers.auth import schemas
from routers.users import service
from database.core import SessionDep
from uuid import UUID


router = APIRouter(
    prefix="/users", 
    tags=["Users"]
)

@router.get("/", response_model=list[schemas.UserBase])
async def get_users(session: SessionDep):
    users = await service.get_users(session)
    return users


@router.get("/{user_id}", response_model=schemas.UserBase)
async def get_user_by_id(user_id: UUID, session: SessionDep):
    user = await service.get_user_by_id(user_id, session)
    return user


@router.put("/{user_id}", response_model=schemas.UserBase)
async def update_user(user_id: UUID, user_update: schemas.UserBase, session: SessionDep):
    updated_user = await service.update_user(user_id, user_update, session)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, session: SessionDep):
    deleted_user = await service.delete_user(user_id, session)
    return deleted_user