from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from .associations import user_favorites, movie_genres

class Movies(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    release_year: Mapped[int] = mapped_column()
    poster_url: Mapped[str] = mapped_column()
    rating: Mapped[float] = mapped_column(default=0.0)

    favorited_by: Mapped[List["Users"]] = relationship(
        secondary=user_favorites,
        back_populates="favorites"
    )

    genres: Mapped[List["Genres"]] = relationship(
        secondary=movie_genres,
        back_populates="movies"
        
    )