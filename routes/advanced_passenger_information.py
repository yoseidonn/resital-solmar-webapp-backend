from fastapi import APIRouter, HTTPException
from schemas import AdvancedPassengerInformationCreate, AdvancedPassengerInformationRead
from typing import List
from services import advanced_passenger_service

router = APIRouter(prefix="/advanced-passenger-informations", tags=["advanced_passenger_informations"])

@router.post("/", response_model=AdvancedPassengerInformationRead)
async def create_advanced_passenger_information(info: AdvancedPassengerInformationCreate):
    obj = await advanced_passenger_service.create(info)
    return await AdvancedPassengerInformationRead.from_tortoise_orm(obj)

@router.get("/", response_model=List[AdvancedPassengerInformationRead])
async def list_advanced_passenger_informations():
    infos = await advanced_passenger_service.list_all()
    return [await AdvancedPassengerInformationRead.from_tortoise_orm(i) for i in infos]

@router.get("/{info_id}", response_model=AdvancedPassengerInformationRead)
async def get_advanced_passenger_information(info_id: int):
    info = await advanced_passenger_service.get_by_id(info_id)
    if not info:
        raise HTTPException(status_code=404, detail="AdvancedPassengerInformation not found")
    return await AdvancedPassengerInformationRead.from_tortoise_orm(info)

@router.put("/{info_id}", response_model=AdvancedPassengerInformationRead)
async def update_advanced_passenger_information(info_id: int, info: AdvancedPassengerInformationCreate):
    obj = await advanced_passenger_service.update(info_id, info)
    if not obj:
        raise HTTPException(status_code=404, detail="AdvancedPassengerInformation not found")
    return await AdvancedPassengerInformationRead.from_tortoise_orm(obj)

@router.delete("/{info_id}")
async def delete_advanced_passenger_information(info_id: int):
    deleted = await advanced_passenger_service.delete(info_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="AdvancedPassengerInformation not found")
    return {"ok": True} 