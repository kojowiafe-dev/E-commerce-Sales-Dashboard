from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from ...models import model
from ...routers.auth import schemas, token_access
from sqlmodel import select
from ...database.core import SessionDep
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import logging

# You would want to store this in an environment variable or a secret manager

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str, session: Session) -> model.User | bool:
    user = session.query(model.User).filter(model.User.email == email).first()
    if not user or not verify_password(password, user.password):
        logging.warning(f"Failed authentication attempt for email: {email}")
        return False
    return user



async def register(
    registration_data: schemas.UserRegister,
    session: SessionDep
):
    try:
        # Check if username already exists
        existing_user = await session.execute(
            select(model.User).where(model.User.name == registration_data.name)
        )
        existing_user = existing_user.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if email already exists
        if registration_data.email:
            existing_email = await session.execute(
                select(model.User).where(model.User.email == registration_data.email)
            )
            existing_email = existing_email.scalars().first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

    
        # Create user
        hashed_password = get_password_hash(registration_data.password)
        db_user = model.User(
            # member_id=db_member.id,
            name=registration_data.name,
            email=registration_data.email,
            role=registration_data.role,
            password=hashed_password
        )

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return db_user

    except Exception as e:
        print(f"Registration error: {str(e)}")  # Debug log
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration."
        )
        
        
async def login(
    form_data: schemas.UserLogin,
    session: SessionDep
):
    # Find user by username
    user = await session.execute(
        select(model.User).where(model.User.name == form_data.name)
    )
    user = user.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Validate role
    if user.role != form_data.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User is not authorized as {form_data.role}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = token_access.create_access_token(
        data={"sub": user.name, "role": user.role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }

    
    
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> schemas.TokenData:
    return token_access.verify_access_token(token)

CurrentUser = Annotated[schemas.TokenData, Depends(get_current_user)]


def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 session: Session) -> schemas.Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect",
                headers={"WWW-Authenticate": "Bearer"},
            )
    token = token_access.create_access_token(user.email, user.id, timedelta(minutes=token_access.ACCESS_TOKEN_EXPIRE_MINUTES))
    return schemas.Token(access_token=token, token_type='bearer')


async def read_users_me(
    current_user: Annotated[model.User, Depends(get_current_user)]
):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching user data: {str(e)}"
        )
        
        
def role_required(required_role: str):
    def role_dependency(current_user: model.User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Only {required_role}s can access this route"
            )
        return current_user
    return role_dependency