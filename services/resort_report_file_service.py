from models import ResortReportFile
from schemas import ResortReportFileCreate
from typing import List, Optional

async def get_by_id(file_id: int) -> Optional[ResortReportFile]:
    return await ResortReportFile.get_or_none(id=file_id)

async def list_all() -> List[ResortReportFile]:
    return await ResortReportFile.all()

async def create(data: ResortReportFileCreate) -> ResortReportFile:
    return await ResortReportFile.create(**data.model_dump())

async def update(file_id: int, data: ResortReportFileCreate) -> Optional[ResortReportFile]:
    obj = await ResortReportFile.get_or_none(id=file_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return obj

async def delete(file_id: int) -> bool:
    deleted = await ResortReportFile.filter(id=file_id).delete()
    return bool(deleted) 