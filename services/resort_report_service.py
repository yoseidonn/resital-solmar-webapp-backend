from models import ResortReport, ResortReportFile
from schemas import ResortReportCreate, ResortReportRead
from typing import List, Optional
from utils.serialization import serialize

async def get_by_id(report_id: int) -> Optional[ResortReportRead]:
    obj = await ResortReport.get_or_none(id=report_id)
    serializer = ResortReportRead.model_validate(obj)
    return await serialize(serializer) if obj else None

async def get_reports_by_file(resort_report_file: ResortReportFile) -> List[ResortReportRead]:
    objs = await ResortReport.filter(resort_report_file=resort_report_file).all()
    serializer = [ResortReportRead.model_validate(o) for o in objs]
    return [await serialize(s) for s in serializer]

async def list_all() -> List[ResortReportRead]:
    objs = await ResortReport.all()
    serializer = [ResortReportRead.model_validate(o) for o in objs]
    return [await serialize(s) for s in serializer]

async def create(data: ResortReportCreate) -> ResortReportRead:
    obj = await ResortReport.create(**data.model_dump())
    serializer = ResortReportRead.model_validate(obj)
    return await serialize(serializer)

async def update(report_id: int, data: ResortReportCreate) -> Optional[ResortReportRead]:
    obj = await ResortReport.get_or_none(id=report_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    serializer = ResortReportRead.model_validate(obj)
    return await serialize(serializer)

async def delete(report_id: int) -> bool:
    deleted = await ResortReport.filter(id=report_id).delete()
    return bool(deleted) 