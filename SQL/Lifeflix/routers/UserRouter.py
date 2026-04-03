from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models.users import Users
from schemas.Movie import Movie
from schemas.User import UpdateUser, User
from utils import get_current_admin, get_current_user
from base import get_object_by_id

router = APIRouter(

    prefix="/users", 
    tags=["User"]
)

@router.get("/me",response_model=User)
def get_my_info(current_user: Users = Depends(get_current_user)):
    return current_user

@router.get("/me/favorites",response_model=list[Movie])
def get_my_favorites(current_user: Users = Depends(get_current_user)):
    return current_user.favorites

@router.patch("/user",response_model=User)
def update_user(updated_data : UpdateUser,db: Session = Depends(get_db),user: Users = Depends(get_current_user)):
    update_dict = updated_data.model_dump(exclude_unset=True)

    if "mail" in update_dict and update_dict["mail"] != user.mail:
        query = select(Users).where(Users.mail == update_dict["mail"])
        existing_user = db.execute(query).scalars().first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="This email already exists")

    
    for key, value in update_dict.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/user/delete",response_model=User)
def delete_user(db: Session = Depends(get_db),current_user: Users = Depends(get_current_user)):
    
    db.delete(current_user)
    db.commit()

    return current_user

@router.delete("/user/delete/{user_id}",response_model=User)
def delete_user_by_admin(user_id: int,db: Session = Depends(get_db),admin: Users = Depends(get_current_admin)):
    user = get_object_by_id(db,Users,user_id)
    
    db.delete(user)
    db.commit()
    
    return user