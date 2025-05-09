from models import AdvancedPassengerInformation
from schemas import AdvancedPassengerInformationCreate
from typing import List, Optional

async def get_by_id(info_id: int) -> Optional[AdvancedPassengerInformation]:
    return await AdvancedPassengerInformation.get_or_none(id=info_id)

async def list_all() -> List[AdvancedPassengerInformation]:
    return await AdvancedPassengerInformation.all()

async def create(data: AdvancedPassengerInformationCreate) -> AdvancedPassengerInformation:
    return await AdvancedPassengerInformation.create(**data.model_dump())

async def update(info_id: int, data: AdvancedPassengerInformationCreate) -> Optional[AdvancedPassengerInformation]:
    obj = await AdvancedPassengerInformation.get_or_none(id=info_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return obj

async def delete(info_id: int) -> bool:
    deleted = await AdvancedPassengerInformation.filter(id=info_id).delete()
    return bool(deleted) 