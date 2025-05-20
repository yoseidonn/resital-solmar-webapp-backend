from pydantic import BaseModel
from datetime import datetime

class CareTakerBase(BaseModel):
    created_at: datetime
    name: str
    phone_number: str

class CareTakerCreate(CareTakerBase):
    pass

class CareTakerRead(CareTakerBase):
    id: int
    class Config:
        from_attributes = True 
