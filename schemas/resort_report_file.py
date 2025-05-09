from pydantic import BaseModel
from datetime import date, datetime

class ResortReportFileBase(BaseModel):
    name: str
    date: date
    file: str

class ResortReportFileCreate(ResortReportFileBase):
    pass

class ResortReportFileRead(ResortReportFileBase):
    id: int
    uploaded_at: datetime
    class Config:
        from_attributes = True 