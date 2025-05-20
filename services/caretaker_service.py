from models import CareTaker
from schemas import CareTakerCreate, CareTakerRead
from typing import List, Optional

async def get_by_id(caretaker_id: int) -> Optional[CareTakerRead]:
    obj = await CareTaker.get_or_none(id=caretaker_id)
    return CareTakerRead.model_validate(obj) if obj else None

async def list_all() -> List[CareTakerRead]:
    objs = await CareTaker.all()
    return [CareTakerRead.model_validate(o) for o in objs]

async def create(data: CareTakerCreate) -> CareTakerRead:
    obj = await CareTaker.create(**data.model_dump())
    return CareTakerRead.model_validate(obj)

async def update(caretaker_id: int, data: CareTakerCreate) -> Optional[CareTakerRead]:
    obj = await CareTaker.get_or_none(id=caretaker_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return CareTakerRead.model_validate(obj)

async def delete(caretaker_id: int) -> bool:
    deleted = await CareTaker.filter(id=caretaker_id).delete()
    return bool(deleted) 