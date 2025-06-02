from models import CareTaker
from schemas import CareTakerCreate, CareTakerRead
from typing import List, Optional
from utils.serialization import serialize

async def get_by_id(caretaker_id: int) -> Optional[CareTakerRead]:
    obj = await CareTaker.get_or_none(id=caretaker_id)
    serializer = CareTakerRead.model_validate(obj)
    assigned_villas = await serialize(obj.assigned_villas)
    serializer.assigned_villas = assigned_villas
    return await serialize(serializer) if obj else None

async def list_all() -> List[CareTakerRead]:
    objs = await CareTaker.all()
    serializer = []
    for o in objs:
        # Handle None case for assigned_villas by defaulting to empty dict
        if o.assigned_villas is None:
            o.assigned_villas = {}
        serializer.append(CareTakerRead.model_validate(o))
    
    for s in serializer:
        assigned_villas = await serialize(s.assigned_villas)
        s.assigned_villas = assigned_villas
    
    return [await serialize(s) for s in serializer]

async def create(data: CareTakerCreate) -> CareTakerRead:
    print(data, type(data))
    data_dict = await serialize(data, exclude_none=True)
    obj = await CareTaker.create(**data_dict)
    serializer = CareTakerRead.model_validate(obj)
    return await serialize(serializer)

async def update(caretaker_id: int, data: CareTakerCreate) -> Optional[CareTakerRead]:
    obj = await CareTaker.get_or_none(id=caretaker_id)
    if not obj:
        return None
    await obj.update_from_dict(data.model_dump())
    await obj.save()
    serializer = CareTakerRead.model_validate(obj)
    return await serialize(serializer)

async def delete(caretaker_id: int) -> bool:
    deleted = await CareTaker.filter(id=caretaker_id).delete()
    return bool(deleted)