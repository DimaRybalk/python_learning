from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime


class User_Model(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True,index=True,)
    hashed_password: Mapped[str] = mapped_column(String(1024))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    balance: Mapped[float] = mapped_column(nullable=False, default=0.0, server_default="0.0")

    refresh_tokens = relationship("Refresh_Model",back_populates="user",cascade="all, delete-orphan")
    portfolio_items = relationship("Portfolio_Model",back_populates="user")
    transaction_items = relationship("Transaction_Model", back_populates="user_model")