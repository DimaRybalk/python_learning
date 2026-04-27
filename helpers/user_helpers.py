
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError,jwt

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from config import ALGORITHM, SECRET_KEY
from database import get_db
from models.user_model import User_Model

security = HTTPBearer()

async def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(security), 
    db: AsyncSession = Depends(get_db)
):
    token = auth.credentials
    exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise exception
    except JWTError:
        raise exception
    
    
    query = (
        select(User_Model)
        .where(User_Model.email == email)
        .options(selectinload(User_Model.portfolio_items))
    )
    
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        raise exception

    return user