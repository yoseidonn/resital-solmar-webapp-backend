async def serialize(obj, exclude_none: bool = False) -> dict:
    if hasattr(obj, 'model_dump'):
        return obj.model_dump(exclude_none=exclude_none)
    elif isinstance(obj, dict):
        return {k: await serialize(v, exclude_none) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [await serialize(v, exclude_none) for v in obj]
    else:
        return obj
