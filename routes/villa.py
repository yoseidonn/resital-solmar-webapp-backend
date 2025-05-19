from fastapi import APIRouter, HTTPException
from schemas import VillaCreate, VillaRead
from models import Villa
from typing import List
from services import villa_service

router = APIRouter()

@router.post("/", response_model=VillaRead)
async def create_villa(villa: VillaCreate):
    obj: Villa = await villa_service.create(villa)
    return VillaRead.model_validate_json(obj.model_dump_json()) 

@router.get("/", response_model=List[VillaRead])
async def list_villas():
    villas = await villa_service.list_all()
    return [VillaRead.model_validate_json(v.model_dump_json()) for v in villas]

@router.get("/{villa_id}", response_model=VillaRead)
async def get_villa(villa_id: int):
    villa = await villa_service.get_by_id(villa_id)
    if not villa:
        raise HTTPException(status_code=404, detail="Villa not found")
    return VillaRead.model_validate_json(villa.model_dump_json())

@router.put("/{villa_id}", response_model=VillaRead)
async def update_villa(villa_id: int, villa: VillaCreate):
    obj = await villa_service.update(villa_id, villa)
    if not obj:
        raise HTTPException(status_code=404, detail="Villa not found")
    return VillaRead.model_validate_json(obj.model_dump_json())

@router.delete("/{villa_id}")
async def delete_villa(villa_id: int):
    deleted = await villa_service.delete(villa_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Villa not found")
    return {"ok": True} 