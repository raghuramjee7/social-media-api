from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import Session
from database import model
from database.pyd_models import PostCreate, PostReturn, UserCreate
from fastapi import APIRouter
from database.connect import get_db
from app.utils import pwd_context, hash_password

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    user.password = hash_password(user.password)
    new_user = model.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Succesfully Created"
    }

@router.get("/", response_model = List[UserCreate])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(model.User).all()

    return users