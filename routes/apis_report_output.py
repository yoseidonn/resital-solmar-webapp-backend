from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import FileResponse
from models import APISReportFile as APISReportFileModel
from schemas.apis_report_output import APISReportOutputGenerateRequest
from schemas.apis_report_output import APISReportOutput
from services import apis_report_output_service
from typing import List
import os

router = APIRouter()

@router.get("/")
async def get_all_outputs():
    outputs = await apis_report_output_service.get_all_outputs()
    return outputs

@router.post("/generate/{file_id}")
async def generate_output(file_id: int, request: APISReportOutputGenerateRequest = Body(...)):
    apis_report_file = await APISReportFileModel.get_or_none(id=file_id)
    if not apis_report_file:
        raise HTTPException(status_code=404, detail="APISReportFile not found")
    return await apis_report_output_service.generate_apis_report_output(apis_report_file, request)

@router.get("/by-file/{file_id}", response_model=List[APISReportOutput])
async def get_outputs_by_file(file_id: int):
    outputs = await apis_report_output_service.get_outputs_by_file(file_id)
    return outputs

@router.get("/download/{output_id}")
async def download_output_file(output_id: str):
    try:
        file_path = await apis_report_output_service.get_file_path(output_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Output file not found")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File does not exist on server")
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=os.path.basename(file_path)) 