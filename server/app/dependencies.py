import models.model as model
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from oauth2 import get_current_user


def role_required(required_role: str):
    def _role_checker(current_user: model.User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{required_role.capitalize()}s only"
            )
        return current_user
    return _role_checker
