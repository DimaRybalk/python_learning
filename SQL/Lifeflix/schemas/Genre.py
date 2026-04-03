from typing import Optional

from pydantic import BaseModel, Field
from enum import Enum


class GenreBase(BaseModel):
    name: str = Field(...)

class CreateGenre(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True

class GenreName(str, Enum):
    ACTION = "Action"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    HORROR = "Horror"
    SCI_FI = "Sci-Fi"

class GenreUpdate(BaseModel):
    name: Optional[str] = Field(None)