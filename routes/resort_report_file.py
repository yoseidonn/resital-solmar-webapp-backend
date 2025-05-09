from fastapi import APIRouter, HTTPException
from schemas import ResortReportFileCreate, ResortReportFileRead
from typing import List
from services import resort_report_file_service

router = APIRouter(prefix="/resort-report-files", tags=["resort_report_files"])

@router.post("/", response_model=ResortReportFileRead)
async def create_resort_report_file(file: ResortReportFileCreate):
    obj = await resort_report_file_service.create(file)
    return await ResortReportFileRead.from_tortoise_orm(obj)

@router.get("/", response_model=List[ResortReportFileRead])
async def list_resort_report_files():
    files = await resort_report_file_service.list_all()
    return [await ResortReportFileRead.from_tortoise_orm(f) for f in files]

@router.get("/{file_id}", response_model=ResortReportFileRead)
async def get_resort_report_file(file_id: int):
    file = await resort_report_file_service.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="ResortReportFile not found")
    return await ResortReportFileRead.from_tortoise_orm(file)

@router.put("/{file_id}", response_model=ResortReportFileRead)
async def update_resort_report_file(file_id: int, file: ResortReportFileCreate):
    obj = await resort_report_file_service.update(file_id, file)
    if not obj:
        raise HTTPException(status_code=404, detail="ResortReportFile not found")
    return await ResortReportFileRead.from_tortoise_orm(obj)

@router.delete("/{file_id}")
async def delete_resort_report_file(file_id: int):
    deleted = await resort_report_file_service.delete(file_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ResortReportFile not found")
    return {"ok": True} 