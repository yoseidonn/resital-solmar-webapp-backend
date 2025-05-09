from fastapi import APIRouter, HTTPException, Body
from models import APISReportFile
from schemas.apis_report_output import APISReportOutputGenerateRequest
from schemas.apis_report_output import APISReportOutputSchema
from services import apis_report_output_service
from typing import List

router = APIRouter(prefix="/apis-report-outputs", tags=["apis_report_outputs"])

@router.post("/generate/{file_id}")
async def generate_output(file_id: int, request: APISReportOutputGenerateRequest = Body(...)):
    apis_report_file = await APISReportFile.get_or_none(id=file_id)
    if not apis_report_file:
        raise HTTPException(status_code=404, detail="APISReportFile not found")
    return await apis_report_output_service.generate_apis_report_output(apis_report_file, request)

@router.get("/by-file/{file_id}", response_model=List[APISReportOutputSchema])
async def get_outputs_by_file(file_id: int):
    outputs = await apis_report_output_service.get_outputs_by_file(file_id)
    return [await APISReportOutputSchema.from_tortoise_orm(o) for o in outputs] 