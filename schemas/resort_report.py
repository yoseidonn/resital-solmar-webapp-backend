from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ResortReportBase(BaseModel):
    accomodation_name: str
    villa_id: Optional[int]
    supplier: str
    resort: str
    opportunity_name: int
    lead_passenger: str
    holiday_start_date: date
    holiday_end_date: date
    total_number_of_passenger: int
    adults: int
    children: int
    infants: int
    flight_arrival_date: date
    flight_arrival_time: datetime
    depature_date: date
    departure_flight_time: datetime
    extras_aggregated: str
    villa_manager_visit_request: str
    live_villa_manager: str
    dt_aff_nane: str
    resort_report_notes: str
    resort_report_file: Optional[int]

class ResortReportCreate(ResortReportBase):
    pass

class ResortReportRead(ResortReportBase):
    id: int
    class Config:
        from_attributes = True 