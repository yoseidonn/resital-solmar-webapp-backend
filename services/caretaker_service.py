from models import CareTaker
from schemas import CareTakerCreate
from typing import List, Optional

async def get_by_id(caretaker_id: int) -> Optional[CareTaker]:
    return await CareTaker.get_or_none(id=caretaker_id)

async def list_all() -> List[CareTaker]:
    return await CareTaker.all()

async def create(data: CareTakerCreate) -> CareTaker:
    return await CareTaker.create(**data.model_dump())

async def update(caretaker_id: int, data: CareTakerCreate) -> Optional[CareTaker]:
    obj = await CareTaker.get_or_none(id=caretaker_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return obj

async def delete(caretaker_id: int) -> bool:
    deleted = await CareTaker.filter(id=caretaker_id).delete()
    return bool(deleted) 