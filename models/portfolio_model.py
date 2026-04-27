from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Portfolio_Model(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    coin_id: Mapped[int] = mapped_column(ForeignKey("coins.id"))
    amount: Mapped[float] = mapped_column(default=0.0)
    added_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    user = relationship("User_Model",back_populates="portfolio_items")
    coin = relationship("Coin_Model", back_populates="portfolio")