from fastapi import APIRouter, HTTPException
from schemas import ResortReportCreate, ResortReportRead
from typing import List
from services import resort_report_service

router = APIRouter(prefix="/resort-reports", tags=["resort_reports"])

@router.post("/", response_model=ResortReportRead)
async def create_resort_report(report: ResortReportCreate):
    obj = await resort_report_service.create(report)
    return await ResortReportRead.from_tortoise_orm(obj)

@router.get("/", response_model=List[ResortReportRead])
async def list_resort_reports():
    reports = await resort_report_service.list_all()
    return [await ResortReportRead.from_tortoise_orm(r) for r in reports]

@router.get("/{report_id}", response_model=ResortReportRead)
async def get_resort_report(report_id: int):
    report = await resort_report_service.get_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="ResortReport not found")
    return await ResortReportRead.from_tortoise_orm(report)

@router.put("/{report_id}", response_model=ResortReportRead)
async def update_resort_report(report_id: int, report: ResortReportCreate):
    obj = await resort_report_service.update(report_id, report)
    if not obj:
        raise HTTPException(status_code=404, detail="ResortReport not found")
    return await ResortReportRead.from_tortoise_orm(obj)

@router.delete("/{report_id}")
async def delete_resort_report(report_id: int):
    deleted = await resort_report_service.delete(report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ResortReport not found")
    return {"ok": True} 