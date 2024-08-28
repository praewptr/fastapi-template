import typing

from sqlmodel import Field, Relationship, SQLModel

if typing.TYPE_CHECKING:
    from .api_key import ApiKey
    from .item import Item


# Shared properties
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None

    # Database model, database table inferred from class name


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")
    api_keys: list["ApiKey"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
