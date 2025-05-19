from fastapi import APIRouter, HTTPException
from schemas import CareTakerCreate, CareTakerRead
from typing import List
from services import caretaker_service

router = APIRouter()

@router.post("/", response_model=CareTakerRead)
async def create_caretaker(caretaker: CareTakerCreate):
    obj = await caretaker_service.create(caretaker)
    return CareTakerRead.model_validate_json(obj.json()) 

@router.get("/", response_model=List[CareTakerRead])
async def list_caretakers():
    caretakers = await caretaker_service.list_all()
    return [CareTakerRead.model_validate_json(c.json()) for c in caretakers]

@router.get("/{caretaker_id}", response_model=CareTakerRead)
async def get_caretaker(caretaker_id: int):
    caretaker = await caretaker_service.get_by_id(caretaker_id)
    if not caretaker:
        raise HTTPException(status_code=404, detail="CareTaker not found")
    return CareTakerRead.model_validate_json(caretaker.json())

@router.put("/{caretaker_id}", response_model=CareTakerRead)
async def update_caretaker(caretaker_id: int, caretaker: CareTakerCreate):
    obj = await caretaker_service.update(caretaker_id, caretaker)
    if not obj:
        raise HTTPException(status_code=404, detail="CareTaker not found")
    return CareTakerRead.model_validate_json(obj.json())

@router.delete("/{caretaker_id}")
async def delete_caretaker(caretaker_id: int):
    deleted = await caretaker_service.delete(caretaker_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="CareTaker not found")
    return {"ok": True} 