from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from base import get_object_by_id
from database import get_db
from models.genres import Genres
from models.users import Users
from schemas.Genre import Genre,CreateGenre, GenreUpdate
from utils import get_current_admin

router = APIRouter(

    prefix="/genres", 
    tags=["Genre"]
)

@router.post("/new_genre",response_model=Genre)
def create_genre(genre_data : CreateGenre ,
    db: Session = Depends(get_db),
    admin: Users = Depends(get_current_admin)):

    query = select(Genres).where(Genres.name == genre_data.name)
    genre = db.execute(query).scalars().first()

    if genre:
        raise HTTPException(status_code=404,detail="This genre already exists")
    
    new_genre = Genres(**genre_data.model_dump())

    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)

    return new_genre

@router.get("/all",response_model=list[Genre])
def get_all_genres(db: Session = Depends(get_db)):
    genres = db.query(Genres).all()
    return genres

@router.patch("/genre/{genre_id}", response_model=Genre)
def update_genre(genre_data : GenreUpdate,genre_id:int,
    db: Session = Depends(get_db),admin: Users = Depends(get_current_admin)):

    genre = get_object_by_id(db,Genres,genre_id)
    
    new_data = genre_data.model_dump(exclude_unset=True)

    for key,value in new_data.items():
        setattr(genre,key,value)

    db.commit()
    db.refresh(genre)

    return genre

@router.delete("/genre/{genre_id}", response_model=Genre)
def delete_genre(genre_id:int,db: Session = Depends(get_db),admin: Users = Depends(get_current_admin)):
    genre = get_object_by_id(db,Genres,genre_id)
    
    db.delete(genre)
    db.commit()

    return genre