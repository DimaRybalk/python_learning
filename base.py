from fastapi import HTTPException
from requests import Session


def get_object_by_id(db: Session, model, obj_id: int):
    obj = db.get(model, obj_id)
    if not obj:
        
        raise HTTPException(
            status_code=404, 
            detail=f"{model.__name__} with id {obj_id} not found"
        )
    
    return obj
