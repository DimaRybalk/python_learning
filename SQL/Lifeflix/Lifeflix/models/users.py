from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from .associations import user_favorites

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    mail: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column() 
    is_admin: Mapped[bool] = mapped_column(default=False)

    favorites: Mapped[List["Movies"]] = relationship(
        secondary=user_favorites,
        back_populates="favorited_by"
        
    )