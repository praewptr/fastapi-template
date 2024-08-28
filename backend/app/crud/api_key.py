import secrets

from sqlmodel import Session, select

from app.core.security import get_password_hash
from app.models import ApiKey, ApiKeyPublic


def create_api_key(*, session: Session, user_id: int) -> ApiKeyPublic:
    gen_key = secrets.token_urlsafe(32)
    hashed_key = get_password_hash(gen_key)

    db_obj = ApiKey(hashed_key=hashed_key, owner_id=user_id)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return ApiKeyPublic(id=db_obj.id, key=gen_key)


def get_api_key_by_user_id(*, session: Session, user_id: int) -> ApiKey | None:
    statement = select(ApiKey).where(ApiKey.owner_id == user_id)
    return session.exec(statement).first()


def regenerate_api_key(*, session: Session, user_id: int) -> ApiKeyPublic:
    api_key = get_api_key_by_user_id(session=session, user_id=user_id)
    if api_key:
        session.delete(api_key)
        session.commit()
    return create_api_key(session=session, user_id=user_id)
