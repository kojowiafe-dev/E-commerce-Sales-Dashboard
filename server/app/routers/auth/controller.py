from typing import Annotated
from fastapi import APIRouter, Depends, Request
from starlette import status
from ...routers.auth import schemas, service
from fastapi.security import OAuth2PasswordRequestForm
from ...database.core import SessionDep
from ...rate_limiter import limiter


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserBase)
@limiter.limit("5/hour")
async def register_user(request: Request, session: SessionDep,
                      register_user_request: schemas.UserRegister):
    registered_user = await service.register(register_user_request, session)
    return registered_user


@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Token)
@limiter.limit("5/hour")
async def login_user(request: Request, session: SessionDep,
                      login_user_request: schemas.UserLogin):
    login_response = await service.login(login_user_request, session)
    return login_response


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 session: SessionDep):
    await service.login_for_access_token(form_data, session)

