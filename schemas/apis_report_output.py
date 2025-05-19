from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any

class IndividualVillaEntry(BaseModel):
    villa_name: str
    holiday_start_date: str
    holiday_end_date: str
    extras_aggregated: str
    opportunity_name: str

class APISReportOutputGenerateRequest(BaseModel):
    opportunity_name: str
    headers: List[str]

class APISReportOutputSchema(BaseModel):
    id: Optional[int]
    apis_report_file: int
    file_path: str
    individual_reservations: Optional[List[Any]]
    created_at: Optional[datetime]
    class Config:
        from_attributes = True 