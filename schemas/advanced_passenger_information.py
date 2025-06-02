from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class AdvancedPassengerInformationBase(BaseModel):
    account_name: str
    country: str
    passenger_name: str
    opportunity_name: int
    accomodation_name: str
    holiday_start_date: date
    holiday_end_date: date
    age: int
    date_of_birth: date
    country_of_issue: str
    document_type: str
    foid_number: str
    foid_issue: datetime
    foid_expiry: datetime
    nationality: str
    villa_id: Optional[int]
    apis_report_file_id: Optional[int]


class AdvancedPassengerInformationCreate(AdvancedPassengerInformationBase):
    pass

class AdvancedPassengerInformationRead(AdvancedPassengerInformationBase):
    id: int
    class Config:
        from_attributes = True 