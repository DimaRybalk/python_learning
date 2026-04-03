from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base


user_favorites = Table(
    "user_favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id",ondelete="CASCADE"), primary_key=True),
    Column("movie_id", Integer, ForeignKey("movies.id",ondelete="CASCADE"), primary_key=True),
)


movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id",ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id",ondelete="CASCADE"), primary_key=True),
)