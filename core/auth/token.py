from datetime import datetime, timedelta
from jose import jwt
from sqlmodel import SQLModel

from config import settings


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenDataCoach(SQLModel):
    email: str | None = None


class TokenDataUserFitbit(SQLModel):
    fitbit_user_id: str | None = None


def create_access_token(data: dict):
    to_encode = data.copy()
    if expires_delta := timedelta(minutes=settings.access_token_expire_minutes):
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
