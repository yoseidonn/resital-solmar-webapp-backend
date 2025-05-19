from models import Villa
from schemas import VillaCreate, VillaRead
from typing import List, Optional

async def get_by_id(villa_id: int) -> Optional[VillaRead]:
    obj = await Villa.get_or_none(id=villa_id)
    return VillaRead.model_validate_json(obj.model_dump_json()) if obj else None

async def list_all() -> List[VillaRead]:
    objs = await Villa.all()
    return [VillaRead.model_validate_json(o.model_dump_json()) for o in objs]

async def create(data: VillaCreate) -> VillaRead:
    obj = await Villa.create(**data.model_dump())
    return VillaRead.model_validate_json(obj.model_dump_json())

async def update(villa_id: int, data: VillaCreate) -> Optional[VillaRead]:
    obj = await Villa.get_or_none(id=villa_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return VillaRead.model_validate_json(obj.model_dump_json())

async def delete(villa_id: int) -> bool:
    deleted = await Villa.filter(id=villa_id).delete()
    return bool(deleted) 