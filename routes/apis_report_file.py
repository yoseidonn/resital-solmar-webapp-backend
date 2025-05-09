from fastapi import APIRouter, HTTPException
from schemas import APISReportFileCreate, APISReportFileRead
from typing import List
from services import apis_report_file_service

router = APIRouter(prefix="/apis-report-files", tags=["apis_report_files"])

@router.post("/", response_model=APISReportFileRead)
async def create_apis_report_file(file: APISReportFileCreate):
    obj = await apis_report_file_service.create(file)
    return await APISReportFileRead.from_tortoise_orm(obj)

@router.get("/", response_model=List[APISReportFileRead])
async def list_apis_report_files():
    files = await apis_report_file_service.list_all()
    return [await APISReportFileRead.from_tortoise_orm(f) for f in files]

@router.get("/{file_id}", response_model=APISReportFileRead)
async def get_apis_report_file(file_id: int):
    file = await apis_report_file_service.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="APISReportFile not found")
    return await APISReportFileRead.from_tortoise_orm(file)

@router.put("/{file_id}", response_model=APISReportFileRead)
async def update_apis_report_file(file_id: int, file: APISReportFileCreate):
    obj = await apis_report_file_service.update(file_id, file)
    if not obj:
        raise HTTPException(status_code=404, detail="APISReportFile not found")
    return await APISReportFileRead.from_tortoise_orm(obj)

@router.delete("/{file_id}")
async def delete_apis_report_file(file_id: int):
    deleted = await apis_report_file_service.delete(file_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="APISReportFile not found")
    return {"ok": True} 