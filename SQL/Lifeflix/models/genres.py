from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from .associations import movie_genres

class Genres(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    movies: Mapped[List["Movies"]] = relationship(
        secondary=movie_genres,
        back_populates="genres"
    )