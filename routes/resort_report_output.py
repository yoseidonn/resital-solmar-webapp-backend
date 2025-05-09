from fastapi import APIRouter, HTTPException
from models import ResortReportFile, ResortReportOutput
from schemas import ResortReportOutputSchema
from services import resort_report_output_service
from typing import List

router = APIRouter(prefix="/resort-report-outputs", tags=["resort_report_outputs"])

@router.post("/generate/{file_id}", response_model=dict)
async def generate_outputs(file_id: int, selected_users: List[dict]):
    resort_report_file = await ResortReportFile.get_or_none(id=file_id)
    if not resort_report_file:
        raise HTTPException(status_code=404, detail="ResortReportFile not found")
    # selected_users should be a list of dicts with .name, .villa_assignments, .rules
    # You may want to validate/parse these into objects as needed
    outputs = await resort_report_output_service.generate_resort_report_output(resort_report_file, selected_users)
    return outputs

@router.get("/by-file/{file_id}", response_model=List[ResortReportOutputSchema])
async def get_outputs_by_file(file_id: int):
    outputs = await resort_report_output_service.get_outputs_by_file(file_id)
    return [await ResortReportOutputSchema.from_tortoise_orm(o) for o in outputs]

@router.get("/", response_model=List[ResortReportOutputSchema])
async def get_all_outputs():
    outputs = await ResortReportOutput.all()
    return [await ResortReportOutputSchema.from_tortoise_orm(o) for o in outputs] 