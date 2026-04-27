from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Transaction_Model(Base):

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    coin_id: Mapped[int] = mapped_column(ForeignKey("coins.id"))
    ticker: Mapped[str] = mapped_column()
    amount: Mapped[float] = mapped_column()
    price_at_runtime: Mapped[float] = mapped_column()
    transaction_type: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    coin_model = relationship("Coin_Model",back_populates="transaction")
    user_model = relationship("User_Model",back_populates="transaction_items")


