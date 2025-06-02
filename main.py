from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from routes import (
    caretaker_router,
    villa_router,
    resort_report_file_router,
    resort_report_router,
    apis_report_file_router,
    advanced_passenger_information_router,
    caretaker_extras_view_output_router,
    apis_report_output_router,
    extras_filtered_reservation_output_router,
)
from database import TORTOISE_ORM

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
    expose_headers=["Content-Length", "Content-Range"],
    max_age=3600
)

app.include_router(caretaker_router, prefix="/caretakers", tags=["Care Takers"])
app.include_router(villa_router, prefix="/villas", tags=["Villas"])
app.include_router(resort_report_file_router, prefix="/resort-report-files", tags=["Resort Report Files"])
app.include_router(resort_report_router, prefix="/resort-reports", tags=["Resort Reports"])
app.include_router(apis_report_file_router, prefix="/apis-report-files", tags=["APIS Report Files"])
app.include_router(advanced_passenger_information_router, prefix="/advanced-passenger-information", tags=["Advanced Passenger Information"])
app.include_router(caretaker_extras_view_output_router, prefix="/caretaker-extras-view-outputs", tags=["Caretaker Extras View Outputs"])
app.include_router(apis_report_output_router, prefix="/apis-report-outputs", tags=["APIS Report Outputs"])
app.include_router(extras_filtered_reservation_output_router, prefix="/extras-filtered-reservation-outputs", tags=["Extras Filtered Reservation Outputs"])

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}