from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any
from schemas.apis_report_output import IndividualVillaEntry

class CaretakerExtrasViewOutputGenerateRequest(BaseModel):
    selected_users: List[Any]
    headers: List[str]
    individual_villa_entries: List[IndividualVillaEntry] = []

class CaretakerExtrasViewOutput(BaseModel):
    id: Optional[int]
    user_name: str
    resort_report_file: int
    content: str
    created_at: Optional[datetime]
    class Config:
        from_attributes = True 
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }