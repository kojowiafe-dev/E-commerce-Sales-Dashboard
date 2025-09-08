from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import jwt, JWTError
from sqlmodel import select
import database, token_access, models.model as model

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")  # Use generic login path

def get_current_user(
    session: database.SessionDep, 
    token: Annotated[str, Depends(oauth2_scheme)]
) -> model.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, token_access.SECRET_KEY, algorithms=[token_access.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(model.User).where(model.User.username == username)).first()
    if user is None:
        raise credentials_exception

    return user

def role_required(required_role: str):
    def role_dependency(current_user: model.User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Only {required_role}s can access this route"
            )
        return current_user
    return role_dependency
