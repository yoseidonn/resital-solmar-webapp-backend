from fastapi import APIRouter, HTTPException
from schemas import CareTakerCreate, CareTakerRead, CareTakerUpdate
from typing import List
from services import caretaker_service

router = APIRouter()

@router.post("/", response_model=CareTakerRead)
async def create_caretaker(caretaker: CareTakerCreate):
    obj = await caretaker_service.create(caretaker)
    return obj

@router.get("/", response_model=List[CareTakerRead])
async def list_caretakers():
    caretakers = await caretaker_service.list_all()
    return caretakers

@router.get("/{caretaker_id}", response_model=CareTakerRead)
async def get_caretaker(caretaker_id: int):
    caretaker = await caretaker_service.get_by_id(caretaker_id)
    if not caretaker:
        raise HTTPException(status_code=404, detail="CareTaker not found")
    return caretaker

@router.put("/{caretaker_id}", response_model=CareTakerRead)
async def update_caretaker(caretaker_id: int, caretaker: CareTakerUpdate):
    obj = await caretaker_service.update(caretaker_id, caretaker)
    if not obj:
        raise HTTPException(status_code=404, detail="CareTaker not found")
    return obj

@router.delete("/{caretaker_id}")
async def delete_caretaker(caretaker_id: int):
    deleted = await caretaker_service.delete(caretaker_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="CareTaker not found")
    return {"success": True} 