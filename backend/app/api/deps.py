import logging
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models import ApiKey, TokenPayload, User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

header_scheme = APIKeyHeader(name="x-key")

logger = logging.getLogger("uvicorn.error")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]
ApiKeyDep = Annotated[str, Depends(header_scheme)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def get_current_user_by_key(session: SessionDep, api_key: ApiKeyDep) -> User:
    api_keys = session.exec(select(ApiKey)).all()
    if not api_keys:
        raise HTTPException(status_code=404, detail="API Key not found")

    if security.verify_api_key(api_key, [key.hashed_key for key in api_keys]):
        return session.get(User, api_keys[0].owner_id)
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")


CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentKey = Annotated[str, Depends(get_current_user_by_key)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
