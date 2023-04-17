from jose import JWTError, jwt
from typing import Dict, Optional
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from config import settings
from db import get_session
from services.coach.models import Coach

from .token import TokenDataCoach

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OAuth2PasswordBearerWithCookieOrHeader(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str | None = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            authorization: str = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(authorization)
            if not authorization or scheme.lower() != "bearer":
                if self.auto_error:
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Not authenticated",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                else:
                    return None
        return param


#  WATCH THIS: The endpoint is absolute no relative, CAREFUL IF YOU CHANGE IT!
oauth2_scheme = OAuth2PasswordBearerWithCookieOrHeader(tokenUrl='admin-coach/login')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db_session, email: str, password: str):
    user = Coach.get_coach_by_email(db_session, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    """
    if not user.verified:
        return False
    """
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db_session=Depends(get_session)) -> Coach:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenDataCoach(email=email)
    except JWTError:
        raise credentials_exception
    user = Coach.get_coach_by_email(db_session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: 'Coach' = Depends(get_current_user)):
    """
    Here should be all the validations to accept an user as active, and therefore, give them rights for login
    :param current_user:
    :return:
    """
    if not current_user.active and not current_user.admin:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
