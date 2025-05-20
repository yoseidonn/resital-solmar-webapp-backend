from models import APISReportFile
from schemas import APISReportFileCreate, APISReportFileRead
from typing import List, Optional

async def get_by_id(file_id: int) -> Optional[APISReportFileRead]:
    obj = await APISReportFile.get_or_none(id=file_id).prefetch_related('advanced_passenger_information')
    return APISReportFileRead.model_validate(obj)

async def list_all() -> List[APISReportFileRead]:
    objs = await APISReportFile.all().prefetch_related('advanced_passenger_information')
    return [APISReportFileRead.model_validate(o) for o in objs]

async def create(data: APISReportFileCreate) -> APISReportFileRead:
    obj = await APISReportFile.create(**data.model_dump())
    return APISReportFileRead.model_validate(obj)

async def update(file_id: int, data: APISReportFileCreate) -> Optional[APISReportFileRead]:
    obj = await APISReportFile.get_or_none(id=file_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return APISReportFileRead.model_validate(obj)

async def delete(file_id: int) -> bool:
    deleted = await APISReportFile.filter(id=file_id).delete()
    return bool(deleted) 