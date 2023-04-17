from fastapi import Header, HTTPException, status, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext

from config import settings
from db import get_session
from services.user_fitbit.models import UserFitbit

from .token import TokenDataUserFitbit

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user(token: str | None = Header(default=None), db_session=Depends(get_session)) -> UserFitbit:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        fitbit_user_id: str = payload.get("sub")
        if fitbit_user_id is None:
            raise credentials_exception
        token_data = TokenDataUserFitbit(fitbit_user_id=fitbit_user_id)
    except JWTError:
        raise credentials_exception
    user = UserFitbit.get_by_fitbit_user_id(db_session, fitbit_user_id=token_data.fitbit_user_id)
    if user is None:
        raise credentials_exception
    return user
