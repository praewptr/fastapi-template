from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import ApiKeyPublic

router = APIRouter()


@router.post("/", response_model=ApiKeyPublic)
def create_api_key(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Create new API key.
    """
    api_key = crud.get_api_key_by_user_id(session=session, user_id=current_user.id)
    if api_key:
        raise HTTPException(
            status_code=400,
            detail="The user already has an API key",
        )
    return crud.create_api_key(session=session, user_id=current_user.id)


# @router.get("/", response_model=Message)
# def read_api_key(current_key: CurrentKey) -> Any:
#     """
#     Read API key.
#     """
#     return {"message": "API key is valid"}


@router.put("/", response_model=ApiKeyPublic)
def regenerate_api_key(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Regenerate API key.
    """
    return crud.regenerate_api_key(session=session, user_id=current_user.id)
