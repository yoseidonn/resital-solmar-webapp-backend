from fastapi import APIRouter, HTTPException, UploadFile, File
import shutil
import os
from schemas import ResortReportFileCreate, ResortReportFileRead
from typing import List
from services import resort_report_file_service

router = APIRouter()

UPLOAD_DIR = "media/resort_report_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_resort_report_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file": file.filename, "file_path": file_location}

@router.post("/", response_model=ResortReportFileRead)
async def create_resort_report_file(file: ResortReportFileCreate):
    obj = await resort_report_file_service.create(file)
    return obj

@router.get("/", response_model=List[ResortReportFileRead])
async def list_resort_report_files():
    files = await resort_report_file_service.list_all()
    return files

@router.get("/{file_id}", response_model=ResortReportFileRead)
async def get_resort_report_file(file_id: int):
    file = await resort_report_file_service.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="ResortReportFile not found")
    return file

@router.put("/{file_id}", response_model=ResortReportFileRead)
async def update_resort_report_file(file_id: int, file: ResortReportFileCreate):
    obj = await resort_report_file_service.update(file_id, file)
    if not obj:
        raise HTTPException(status_code=404, detail="ResortReportFile not found")
    return obj

@router.delete("/{file_id}")
async def delete_resort_report_file(file_id: int):
    deleted = await resort_report_file_service.delete(file_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ResortReportFile not found")
    return {"ok": True} 