from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from sqlalchemy import ForeignKey, func

class Measurement(Base):
    __tablename__ = "measurements"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column()
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

    device: Mapped["Device"] = relationship(back_populates="measurements")


class Device(Base):
    __tablename__ = "devices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    type: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(default="off")
    
    measurements: Mapped[list["Measurement"]] = relationship(
        back_populates="device", 
        lazy="selectin",
        cascade="all, delete-orphan"
    )

class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(index=True)
    treshold: Mapped[float] = mapped_column()
    operator: Mapped[str] = mapped_column()
    action_device_id: Mapped[int] = mapped_column(index=True)
    action_value: Mapped[str] = mapped_column()