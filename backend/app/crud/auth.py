import secrets

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import ApiKey, ApiKeyPublic, User

from .user import get_user_by_email


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_api_key(*, session: Session, user_id: int) -> ApiKeyPublic:
    gen_key = secrets.token_urlsafe(32)
    hashed_key = get_password_hash(gen_key)

    db_obj = ApiKey(hashed_key=hashed_key, owner_id=user_id)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return ApiKeyPublic(id=db_obj.id, key=gen_key)


def get_api_key_by_user_id(*, session: Session, user_id: int) -> ApiKey | None:
    return session.exec(select(ApiKey).filter(ApiKey.owner_id == user_id)).first()
