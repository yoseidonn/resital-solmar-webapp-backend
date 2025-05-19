from fastapi import APIRouter, HTTPException
from schemas import VillaCreate, VillaRead
from models import Villa
from typing import List
from services import villa_service

router = APIRouter()

@router.post("/", response_model=VillaRead)
async def create_villa(villa: VillaCreate):
    obj = await villa_service.create(villa)
    return obj

@router.get("/", response_model=List[VillaRead])
async def list_villas():
    villas = await villa_service.list_all()
    return villas

@router.get("/{villa_id}", response_model=VillaRead)
async def get_villa(villa_id: int):
    villa = await villa_service.get_by_id(villa_id)
    if not villa:
        raise HTTPException(status_code=404, detail="Villa not found")
    return villa

@router.put("/{villa_id}", response_model=VillaRead)
async def update_villa(villa_id: int, villa: VillaCreate):
    obj = await villa_service.update(villa_id, villa)
    if not obj:
        raise HTTPException(status_code=404, detail="Villa not found")
    return obj

@router.delete("/{villa_id}")
async def delete_villa(villa_id: int):
    deleted = await villa_service.delete(villa_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Villa not found")
    return {"ok": True} 