from models import CareTaker
from schemas import CareTakerCreate, CareTakerRead
from typing import List, Optional

async def get_by_id(caretaker_id: int) -> Optional[CareTakerRead]:
    obj = await CareTaker.get_or_none(id=caretaker_id)
    return CareTakerRead.model_validate_json(obj.model_dump_json()) if obj else None

async def list_all() -> List[CareTakerRead]:
    objs = await CareTaker.all()
    return [CareTakerRead.model_validate_json(o.model_dump_json()) for o in objs]

async def create(data: CareTakerCreate) -> CareTakerRead:
    obj = await CareTaker.create(**data.model_dump())
    return CareTakerRead.model_validate_json(obj.model_dump_json())

async def update(caretaker_id: int, data: CareTakerCreate) -> Optional[CareTakerRead]:
    obj = await CareTaker.get_or_none(id=caretaker_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    return CareTakerRead.model_validate_json(obj.model_dump_json())

async def delete(caretaker_id: int) -> bool:
    deleted = await CareTaker.filter(id=caretaker_id).delete()
    return bool(deleted) 