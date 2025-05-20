from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List, Any
from schemas.apis_report_output import IndividualVillaEntry

class ExtrasFilteredReservationOutputGenerateRequest(BaseModel):
    filters: Dict[str, List[str]]
    headers: List[str]
    individual_villa_entries: List[IndividualVillaEntry] = []

class ExtrasFilteredReservationOutput(BaseModel):
    id: Optional[str]
    resort_report_file: int
    file_name: str
    generated_date: datetime
    applied_filters: Optional[Dict[str, List[str]]]
    grouped_reservations: Optional[Dict[str, Any]]
    file_path: Optional[str]
    created_at: Optional[datetime]
    class Config:
        from_attributes = True 
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }