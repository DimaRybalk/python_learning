from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.users import Users
from schemas.User import User,CreateUser,LoginUser
from utils import create_access_token, get_current_user, hash_password, verify_password

router = APIRouter(

    prefix="/auth", 
    tags=["Authentication"]
    
)

@router.post("/register",response_model=User)
def create_user(userdata: CreateUser,db: Session = Depends(get_db)):
    user_exists = db.query(Users).filter(Users.mail == userdata.mail).first()

    if user_exists:
        raise HTTPException(status_code=400,detail="User already exists")
    
    hashed_password_new =  hash_password(userdata.password)

    new_user = Users(
        name = userdata.name,
        mail = userdata.mail,
        hashed_password = hashed_password_new
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail="Error while saving data")
    return new_user


@router.post("/login")
def login(userdata: LoginUser, db: Session = Depends(get_db)):
    user_exists = db.query(Users).filter(Users.mail == userdata.mail).first()

    if not user_exists:
        raise HTTPException(status_code=401,detail="User with this data doesn't exist")
    
    if not verify_password(userdata.password, user_exists.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong mail or password")
    
    access_token = create_access_token(data={"sub": user_exists.mail})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user",response_model=User)
def auth_current_user(current_user : Users = Depends(get_current_user)):
    return current_user