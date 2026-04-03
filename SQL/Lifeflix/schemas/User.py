from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    name : str = Field(..., min_length=5,max_length=25)
    mail: EmailStr = Field(...)

class CreateUser(UserBase):
    password: str = Field(...,min_length=8,max_length=72)

class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

class LoginUser(BaseModel):
    mail: EmailStr = Field(...)
    password: str = Field(...)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UpdateUser(BaseModel):
    name : Optional[str] = Field(None, min_length=5,max_length=25)
    mail: Optional[EmailStr] = Field(None)
    is_admin: Optional[bool] = Field(default=False)