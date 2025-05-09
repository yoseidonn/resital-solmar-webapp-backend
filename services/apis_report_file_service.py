from models import APISReportFile
from schemas import APISReportFileCreate
from typing import List, Optional

async def get_by_id(file_id: int) -> Optional[APISReportFile]:
    return await APISReportFile.get_or_none(id=file_id)

async def list_all() -> List[APISReportFile]:
    return await APISReportFile.all()

async def create(data: APISReportFileCreate) -> APISReportFile:
    return await APISReportFile.create(**data.model_dump())

async def update(file_id: int, data: APISReportFileCreate) -> Optional[APISReportFile]:
    obj = await APISReportFile.get_or_none(id=file_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return obj

async def delete(file_id: int) -> bool:
    deleted = await APISReportFile.filter(id=file_id).delete()
    return bool(deleted) 