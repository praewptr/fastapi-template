from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class ApiKeyBase(SQLModel):
    hashed_key: str


class ApiKey(ApiKeyBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: Optional["User"] = Relationship(back_populates="api_keys")


class ApiKeyPublic(SQLModel):
    id: int
    key: str
