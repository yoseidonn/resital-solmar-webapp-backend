from fastapi import APIRouter, HTTPException, Body
from models import ResortReportFile, CaretakerExtrasViewOutput
from schemas.caretaker_extras_view_output import CaretakerExtrasViewOutputSchema, CaretakerExtrasViewOutputGenerateRequest  
from services.caretaker_extras_view_output_service import generate_caretaker_extras_view_output, get_outputs_by_file
from typing import List

router = APIRouter()

@router.post("/generate/{file_id}", response_model=dict)
async def generate_outputs(file_id: int, body: CaretakerExtrasViewOutputGenerateRequest = Body(...)):
    resort_report_file = await ResortReportFile.get_or_none(id=file_id)
    if not resort_report_file:
        raise HTTPException(status_code=404, detail="ResortReportFile not found")
    outputs = await generate_caretaker_extras_view_output(
        resort_report_file,
        body.selected_users,
        body.headers,
        body.individual_villa_entries
    )
    return outputs

@router.get("/by-file/{file_id}", response_model=List[CaretakerExtrasViewOutputSchema])
async def get_outputs_by_file(file_id: int):
    outputs = await get_outputs_by_file(file_id)
    return [CaretakerExtrasViewOutputSchema.model_validate_json(o.json()) for o in outputs]

@router.get("/", response_model=List[CaretakerExtrasViewOutputSchema])
async def get_all_outputs():
    outputs = await CaretakerExtrasViewOutput.all()
    return [CaretakerExtrasViewOutputSchema.model_validate_json(o.json()) for o in outputs] 