from models import AdvancedPassengerInformation
from schemas import AdvancedPassengerInformationCreate, AdvancedPassengerInformationRead
from typing import List, Optional
from utils.serialization import serialize

async def get_by_id(info_id: int) -> Optional[AdvancedPassengerInformationRead]:
    obj = await AdvancedPassengerInformation.get_or_none(id=info_id)
    if not obj:
        return None
    
    serializer = AdvancedPassengerInformationRead.model_validate(obj)
    return await serialize(serializer)

async def list_all() -> List[AdvancedPassengerInformationRead]:
    objs = await AdvancedPassengerInformation.all()
    return [await serialize(AdvancedPassengerInformationRead.model_validate(o)) for o in objs]

async def create(data: AdvancedPassengerInformationCreate) -> AdvancedPassengerInformationRead:
    obj = await AdvancedPassengerInformation.create(**data.model_dump())
    return await serialize(AdvancedPassengerInformationRead.model_validate(obj))

async def update(info_id: int, data: AdvancedPassengerInformationCreate) -> Optional[AdvancedPassengerInformationRead]:
    obj = await AdvancedPassengerInformation.get_or_none(id=info_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return await serialize(AdvancedPassengerInformationRead.model_validate(obj))

async def delete(info_id: int) -> bool:
    deleted = await AdvancedPassengerInformation.filter(id=info_id).delete()
    return bool(deleted) 