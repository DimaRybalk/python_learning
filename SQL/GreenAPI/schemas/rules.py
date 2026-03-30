from typing import Literal, Optional
from pydantic import BaseModel, Field

class BaseRule(BaseModel):
    treshold: float = Field(...,gt=-100,le=500)
    operator: Literal[">","<","=="]
    action_value: float = Field(...,gt=-100,le=500) 
    sensor_id: int
    action_device_id: int

class RuleCreate(BaseRule):
    pass    


class RuleUpdate(BaseModel):
    treshold: Optional[float] = Field(None,gt=-100,le=500)
    operator: Optional[Literal[">","<","=="]]
    action_value: Optional[float] = Field(None,gt=-100,le=500) 
    

class Rule(BaseRule):
    id: int
        

    class Config:
        from_attributes = True