from pydantic import BaseModel, Field, EmailStr,field_validator
from typing import Annotated, Optional
from datetime import datetime, timezone


class BaseUser(BaseModel):

    email: Annotated[
        EmailStr,
        Field(
            ...,
            title="Email",
            description="User email address"
        )
    ]

    password: Annotated[
        str,
        Field(
            ...,
            min_length=5,
            max_length=20
        )
    ]

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain uppercase letter")

        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain digit")

        return value


class User(BaseUser):
    id: int

class UserLogin(BaseModel):
    email: str
    password: str

class CreateUser(BaseUser):
    pass


class BaseTask(BaseModel):
    name: Annotated[
        str,
        Field(
            ...,
            title="Name of the task",
            min_length=1,
            max_length=100
        )
    ]

    description: Annotated[
        Optional[str],
        Field(
            None,
            title="Description of the task",
            max_length=200
        )
    ]


class CreateTask(BaseTask):
    user_id: int


class Task(BaseTask):
    id: int
    user_id: int
    is_complete: bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    model_config = {"from_attributes": True}