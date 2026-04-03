from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session,selectinload

from database import get_db
from models.genres import Genres
from models.movies import Movies
from models.users import Users
from schemas.Genre import GenreName
from schemas.Movie import Movie,CreateMovie, MovieUpdate
from utils import get_current_admin, get_current_user
from base import get_object_by_id


router = APIRouter(

    prefix="/movies", 
    tags=["Movie"]
)

@router.post("/new_movie",response_model=Movie)
def create_new_movie(moviedata: CreateMovie, 
    db: Session = Depends(get_db), admin: Users = Depends(get_current_admin)):

    query = select(Movies).where(Movies.title == moviedata.title)
    movie = db.execute(query).scalars().first()

    if movie:
        raise HTTPException(status_code=404,detail="This movie already exists")

    new_movie = Movies(**moviedata.model_dump(exclude={"genres_names"}))

    db_genres = db.query(Genres).filter(Genres.name.in_(moviedata.genres_names)).all()
    if len(db_genres) != len(moviedata.genres_names):
            found_names = [g.name for g in db_genres]
            missing = set(moviedata.genres_names) - set(found_names)
            raise HTTPException(
                status_code=400, 
                detail=f"Can't find next genres: {list(missing)}. firstly create them in /genres/"
            )
    new_movie.genres = db_genres


    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie



@router.get("/all",response_model=list[Movie])
def get_all_movies(db: Session = Depends(get_db),limit: int = 10,skip: int = 0):
    movies = db.query(Movies).options(selectinload(Movies.genres)).offset(skip).limit(limit).all()

    return movies



@router.get("/movie/{movie_id}",response_model=Movie)
def get_one_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = get_object_by_id(db,Movies,movie_id)
    
    return movie



@router.get("/movie",response_model=list[Movie])
def search_movie_with_title(title:str,db: Session = Depends(get_db)):
    movies = db.query(Movies).options(selectinload(Movies.genres)).filter(Movies.title.ilike(f"%{title}%")).all()

    return movies

@router.get("/movie/filter", response_model=list[Movie])
def search_movie_by_genres( genres: List[GenreName]= Query(None, description="Choose genre"),db: Session = Depends(get_db)):

    query = db.query(Movies).join(Movies.genres)
    
    if genres:
        normalized_genres = [g.capitalize() for g in genres]
        query = query.filter(Genres.name.in_(normalized_genres))

    return query.distinct().all()



@router.patch("/movie/{movie_id}",response_model=Movie)
def update_movie(
    updated_movie : MovieUpdate ,movie_id: int, 
    db: Session = Depends(get_db),
    admin: Users = Depends(get_current_admin)):

    movie = db.query(Movies).where(Movies.id == movie_id).options(selectinload(Movies.genres)).first()

    if not movie:
        raise HTTPException(status_code=404,detail="Movie with this id doesn't exist")
    
    new_data = updated_movie.model_dump(exclude_unset = True)

    for key,value in new_data.items():
        setattr(movie,key,value)

    db.commit()
    db.refresh(movie)

    return movie



@router.delete("/movie/{movie_id}",response_model=Movie)
def delete_movie_by_id(movie_id: int, db: Session = Depends(get_db),admin: Users = Depends(get_current_admin)):
    movie = db.query(Movies).where(Movies.id == movie_id).options(selectinload(Movies.genres)).first()

    if not movie:
        raise HTTPException(status_code=404,detail="Movie with this id doesn't exist")
    
    db.delete(movie)
    db.commit()

    return movie



@router.post("/movie/{movie_id}/favorite")
def toggle_favorite(
    movie_id: int, 
    db: Session = Depends(get_db), 
    current_user: Users = Depends(get_current_user)
):
    movie = db.query(Movies).where(Movies.id == movie_id).options(selectinload(Movies.genres)).first()

    if not movie:
        raise HTTPException(status_code=404,detail="Movie with this id doesn't exist")
    
    if movie not in current_user.favorites:
        current_user.favorites.append(movie)
        status = "added"
    else:
        current_user.favorites.remove(movie)
        status = "removed"

    db.commit()
    db.refresh(current_user)

    return {"status" : status}
    

                       