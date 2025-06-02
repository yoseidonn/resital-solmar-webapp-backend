from models import Villa
from schemas import VillaCreate, VillaRead
from typing import List, Optional
from utils.serialization import serialize

async def get_by_id(villa_id: int) -> Optional[VillaRead]:
    obj = await Villa.get_or_none(id=villa_id)
    serializer = VillaRead.model_validate(obj)
    return await serialize(serializer) if obj else None

async def list_all() -> List[VillaRead]:
    objs = await Villa.all()
    serializer = [VillaRead.model_validate(o) for o in objs]
    return [await serialize(s) for s in serializer]

async def create(data: VillaCreate) -> VillaRead:
    obj = await Villa.create(**data.model_dump())
    serializer = VillaRead.model_validate(obj)
    return await serialize(serializer)

async def update(villa_id: int, data: VillaCreate) -> Optional[VillaRead]:
    obj = await Villa.get_or_none(id=villa_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    serializer = VillaRead.model_validate(obj)
    return await serialize(serializer)

async def delete(villa_id: int) -> bool:
    deleted = await Villa.filter(id=villa_id).delete()
    return bool(deleted) 