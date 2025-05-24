from models import APISReportFile as APISReportFileModel
from schemas import APISReportFileCreate, APISReportFileRead
from typing import List, Optional

async def get_by_id(file_id: int) -> Optional[APISReportFileRead]:
    obj = await APISReportFileModel.get_or_none(id=file_id)
    return APISReportFileRead.model_validate(obj)

async def list_all() -> List[APISReportFileRead]:
    objs = await APISReportFileModel.all()
    return [APISReportFileRead.model_validate(o) for o in objs]

async def create(data: APISReportFileCreate) -> APISReportFileRead:
    obj = await APISReportFileModel.create(**data.model_dump())
    return APISReportFileRead.model_validate(obj)

async def update(file_id: int, data: APISReportFileCreate) -> Optional[APISReportFileRead]:
    obj = await APISReportFileModel.get_or_none(id=file_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return APISReportFileRead.model_validate(obj)

async def delete(file_id: int) -> bool:
    deleted = await APISReportFileModel.filter(id=file_id).delete()
    return bool(deleted) 