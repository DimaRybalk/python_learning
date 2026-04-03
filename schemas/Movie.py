from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

current_year = datetime.now().year

class MovieBase(BaseModel):
    title: str = Field(..., min_length=3,max_length=40)
    description: Optional[str] = Field(None,max_length=500)
    release_year: Optional[int] = Field(None,le=current_year,gt=1895)
    poster_url: Optional[str]

    @field_validator('release_year')
    @classmethod
    def check_year(cls, v):
        if v is not None and v < 1895:
            raise ValueError('Too early for movies!')
        return v


class CreateMovie(MovieBase):
    genres_names: list[str]

class MovieUpdate(MovieBase):
    title: Optional[str] = Field(None,min_length=3,max_length=40)
    description: Optional[str] = Field(None,min_length=3,max_length=500)
    release_year: Optional[int] = Field(None,le=current_year,gt=1895)
    poster_url: Optional[str]

class Movie(MovieBase):
    id: int
    rating: float

    class Config:
        from_attributes = True