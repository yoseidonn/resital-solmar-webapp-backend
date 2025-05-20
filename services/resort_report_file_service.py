from models import ResortReportFile
from schemas import ResortReportFileCreate, ResortReportFileRead
from typing import List, Optional

async def get_by_id(file_id: int) -> Optional[ResortReportFileRead]:
    obj = await ResortReportFile.get_or_none(id=file_id)
    return ResortReportFileRead.model_validate(obj) if obj else None

async def list_all() -> List[ResortReportFileRead]:
    objs = await ResortReportFile.all()
    return [ResortReportFileRead.model_validate(o) for o in objs]

async def create(data: ResortReportFileCreate) -> ResortReportFileRead:
    obj = await ResortReportFile.create(**data.model_dump())
    return ResortReportFileRead.model_validate(obj)

async def update(file_id: int, data: ResortReportFileCreate) -> Optional[ResortReportFileRead]:
    obj = await ResortReportFile.get_or_none(id=file_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return ResortReportFileRead.model_validate(obj)

async def delete(file_id: int) -> bool:
    deleted = await ResortReportFile.filter(id=file_id).delete()
    return bool(deleted) 