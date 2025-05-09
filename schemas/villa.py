from pydantic import BaseModel

class VillaBase(BaseModel):
    villa_name: str
    care_taker: int

class VillaCreate(VillaBase):
    pass

class VillaRead(VillaBase):
    id: int
    class Config:
        from_attributes = True 