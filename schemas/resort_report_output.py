from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResortReportOutputSchema(BaseModel):
    id: Optional[int]
    user_name: str
    resort_report_file: int
    content: str
    created_at: Optional[datetime]
    class Config:
        from_attributes = True 