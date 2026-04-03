import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

class UserBase(BaseModel):
    name : str = Field(..., min_length=5,max_length=25)
    mail: EmailStr = Field(...)

class CreateUser(UserBase):
    password: str = Field(...,min_length=8,max_length=72)

    @field_validator('password')
    @classmethod
    def password_complexity(cls, v: str):
    
        if not re.search(r'\d', v):
            raise ValueError("Password should contain at least one digit")
        
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password should contain at least one Upper Case letter")
            
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password should contain at least one special symbol")
            
        return v

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