from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connect import get_db
from database.pyd_models import UserCreate
from database import model
from app.utils import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login")
async def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(model.User).filter(model.User.email == credentials.username).first()
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = "Invalid Credentials"
        )
        
    
    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = "Invalid Credentials"
        )
    
    #create token
    data = {
        "user_id": user.id
    }
    token = create_access_token(data)

    return {
        "message": "Login Successful",
        "token_type": "bearer",
        "token": token
    }
    
    
