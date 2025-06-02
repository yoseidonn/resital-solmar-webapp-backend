from pydantic import BaseModel
from datetime import datetime

class CareTakerBase(BaseModel):
    name: str
    phone_number: str

class CareTakerCreate(CareTakerBase):
    assigned_villas: dict[int, list[str]]

class CareTakerUpdate(CareTakerBase):
    id: int
    assigned_villas: dict[int, list[str]]

class CareTakerRead(CareTakerBase):
    id: int
    assigned_villas: dict[int, list[str]]
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True 
