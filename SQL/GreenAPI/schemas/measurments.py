from datetime import datetime
from pydantic import BaseModel, Field

class BaseMeasurement(BaseModel):
    value: float = Field(...,gt=-100,lt=500)
    device_id: int = Field(...)

class Measurement(BaseMeasurement):
    id: int
    timestamp: datetime
    

    class Config:
        from_attributes = True

class MeasurementCreate(BaseMeasurement):
    pass