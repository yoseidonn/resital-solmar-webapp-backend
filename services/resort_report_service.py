from models import ResortReport
from schemas import ResortReportCreate
from typing import List, Optional

async def get_by_id(report_id: int) -> Optional[ResortReport]:
    return await ResortReport.get_or_none(id=report_id)

async def list_all() -> List[ResortReport]:
    return await ResortReport.all()

async def create(data: ResortReportCreate) -> ResortReport:
    return await ResortReport.create(**data.model_dump())

async def update(report_id: int, data: ResortReportCreate) -> Optional[ResortReport]:
    obj = await ResortReport.get_or_none(id=report_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return obj

async def delete(report_id: int) -> bool:
    deleted = await ResortReport.filter(id=report_id).delete()
    return bool(deleted) 