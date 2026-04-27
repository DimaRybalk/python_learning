from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime


class Coin_Model(Base):

    __tablename__ = "coins"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    ticker: Mapped[str] = mapped_column(unique=True,nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    coingecko_id: Mapped[str] = mapped_column(unique=True)

    portfolio = relationship("Portfolio_Model", back_populates="coin")
    transaction = relationship("Transaction_Model", back_populates="coin_model")