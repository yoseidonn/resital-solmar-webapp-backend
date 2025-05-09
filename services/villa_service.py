from models import Villa
from schemas import VillaCreate
from typing import List, Optional

async def get_by_id(villa_id: int) -> Optional[Villa]:
    return await Villa.get_or_none(id=villa_id)

async def list_all() -> List[Villa]:
    return await Villa.all()

async def create(data: VillaCreate) -> Villa:
    return await Villa.create(**data.model_dump())

async def update(villa_id: int, data: VillaCreate) -> Optional[Villa]:
    obj = await Villa.get_or_none(id=villa_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return obj

async def delete(villa_id: int) -> bool:
    deleted = await Villa.filter(id=villa_id).delete()
    return bool(deleted) 