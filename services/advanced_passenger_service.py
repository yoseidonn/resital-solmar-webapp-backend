from models import AdvancedPassengerInformation
from schemas import AdvancedPassengerInformationCreate, AdvancedPassengerInformationRead
from typing import List, Optional

async def get_by_id(info_id: int) -> Optional[AdvancedPassengerInformationRead]:
    obj = await AdvancedPassengerInformation.get_or_none(id=info_id).prefetch_related('apis_report_file', 'resort_report_file', 'villa')
    return AdvancedPassengerInformationRead(obj)

async def list_all() -> List[AdvancedPassengerInformationRead]:
    objs = await AdvancedPassengerInformation.all().prefetch_related('apis_report_file', 'resort_report_file', 'villa')
    return [AdvancedPassengerInformationRead(o) for o in objs]

async def create(data: AdvancedPassengerInformationCreate) -> AdvancedPassengerInformationRead:
    obj = await AdvancedPassengerInformation.create(**data.model_dump())
    return AdvancedPassengerInformationRead(obj)

async def update(info_id: int, data: AdvancedPassengerInformationCreate) -> Optional[AdvancedPassengerInformationRead]:
    obj = await AdvancedPassengerInformation.get_or_none(id=info_id).prefetch_related('apis_report_file', 'resort_report_file', 'villa')
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return AdvancedPassengerInformationRead(obj)

async def delete(info_id: int) -> bool:
    deleted = await AdvancedPassengerInformation.filter(id=info_id).delete()
    return bool(deleted) 