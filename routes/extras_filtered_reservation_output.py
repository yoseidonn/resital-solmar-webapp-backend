from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import FileResponse
from models import ResortReportFile, ExtrasFilteredReservationOutput
from schemas import ExtrasFilteredReservationOutputSchema
from services import extras_filtered_reservation_output_service
from typing import List, Dict
import os

router = APIRouter()

@router.get("/")
async def get_all_outputs():
    outputs = await extras_filtered_reservation_output_service.get_all_outputs()
    return outputs

@router.post("/generate/{file_id}", response_model=dict)
async def generate_output(file_id: int, body: Dict = Body(...)):
    # body should contain 'filters' (dict), 'headers' (list), and 'individual_villa_entries' (list)
    filters = body.get('filters', {})
    headers = body.get('headers', [])
    individual_villa_entries = body.get('individual_villa_entries', [])
    resort_report_file = await ResortReportFile.get_or_none(id=file_id)
    if not resort_report_file:
        raise HTTPException(status_code=404, detail="ResortReportFile not found")
    result = await extras_filtered_reservation_output_service.generate_extras_filtered_reservation_summary(resort_report_file, filters, headers, individual_villa_entries)
    return result

@router.get("/by-file/{file_id}", response_model=List[ExtrasFilteredReservationOutputSchema])
async def get_outputs_by_file(file_id: int):
    outputs = await extras_filtered_reservation_output_service.get_outputs_by_file(file_id)
    return outputs

@router.get("/download/{output_id}")
async def download_output_file(output_id: str):
    try:
        file_path = await extras_filtered_reservation_output_service.get_file_path(output_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Output file not found")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File does not exist on server")
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=os.path.basename(file_path)) 