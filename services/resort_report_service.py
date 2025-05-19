from models import ResortReport, ResortReportFile
from schemas import ResortReportCreate, ResortReportRead
from typing import List, Optional

async def get_by_id(report_id: int) -> Optional[ResortReportRead]:
    obj = await ResortReport.get_or_none(id=report_id)
    return ResortReportRead(obj) if obj else None

async def get_reports_by_file(resort_report_file: ResortReportFile) -> List[ResortReportRead]:
    objs = await ResortReport.filter(resort_report_file=resort_report_file).all()
    return [ResortReportRead(o) for o in objs]

async def list_all() -> List[ResortReportRead]:
    objs = await ResortReport.all()
    return [ResortReportRead(o) for o in objs]

async def create(data: ResortReportCreate) -> ResortReportRead:
    obj = await ResortReport.create(**data.model_dump())
    return ResortReportRead(obj)

async def update(report_id: int, data: ResortReportCreate) -> Optional[ResortReportRead]:
    obj = await ResortReport.get_or_none(id=report_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return ResortReportRead(obj)

async def delete(report_id: int) -> bool:
    deleted = await ResortReport.filter(id=report_id).delete()
    return bool(deleted) 