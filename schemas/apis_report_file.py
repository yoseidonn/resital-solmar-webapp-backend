from pydantic import BaseModel
from datetime import date, datetime

class APISReportFileBase(BaseModel):
    name: str
    date: date
    file: str

class APISReportFileCreate(APISReportFileBase):
    pass

class APISReportFileRead(APISReportFileBase):
    id: int
    uploaded_at: datetime
    class Config:
        from_attributes = True 