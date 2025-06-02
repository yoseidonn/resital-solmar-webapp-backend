from models import ResortReportFile
from schemas import ResortReportFileCreate, ResortReportFileRead
from typing import List, Optional
from utils.serialization import serialize

async def get_by_id(file_id: int) -> Optional[ResortReportFileRead]:
    obj = await ResortReportFile.get_or_none(id=file_id)
    serializer = ResortReportFileRead.model_validate(obj)
    return await serialize(serializer) if obj else None

async def list_all() -> List[ResortReportFileRead]:
    objs = await ResortReportFile.all()
    serializer = [ResortReportFileRead.model_validate(o) for o in objs]
    return [await serialize(s) for s in serializer]

async def create(data: ResortReportFileCreate) -> ResortReportFileRead:
    obj = await ResortReportFile.create(**data.model_dump())
    serializer = ResortReportFileRead.model_validate(obj)
    return await serialize(serializer)

async def update(file_id: int, data: ResortReportFileCreate) -> Optional[ResortReportFileRead]:
    obj = await ResortReportFile.get_or_none(id=file_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    serializer = ResortReportFileRead.model_validate(obj)
    return await serialize(serializer)

async def delete(file_id: int) -> bool:
    deleted = await ResortReportFile.filter(id=file_id).delete()
    return bool(deleted) 