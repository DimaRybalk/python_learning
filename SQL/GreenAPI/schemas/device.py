from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

from schemas.measurments import Measurement

class DeviceStatus(str, Enum):
    on = "on"
    off = "off"
    error = "error"


class BaseDevice(BaseModel):
    name: str = Field(...,min_length=3,max_length=100)
    type: str = Field(...,min_length=3,max_length=100)
    

class DeviceCreate(BaseDevice):
    pass    

class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None,min_length=3,max_length=100)
    type: Optional[str] = Field(None,min_length=3,max_length=100)
    status: Optional[DeviceStatus]


class DeviceStats(BaseModel):
    average: Optional[float]
    maximum: Optional[float]
    minimum: Optional[float]
    count: int

class Device(BaseDevice):
    id: int
    status: DeviceStatus = DeviceStatus.off

    measurements: list[Measurement] = []

    class Config:
        from_attributes = True

