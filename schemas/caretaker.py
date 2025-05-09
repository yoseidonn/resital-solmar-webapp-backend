from pydantic import BaseModel

class CareTakerBase(BaseModel):
    name: str
    phone_number: str

class CareTakerCreate(CareTakerBase):
    pass

class CareTakerRead(CareTakerBase):
    id: int
    class Config:
        from_attributes = True 