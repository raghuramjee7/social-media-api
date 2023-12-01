from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from database.pyd_models import TokenData
from database.model import User
from database.connect import get_db
from sqlalchemy.orm import Session
from app.config import settings


oaut2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):

    # create a copy of data
    data_to_encode = data.copy()

    # set expire time
    expire_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({
        "exp": expire_time
    })

    jwt_token = jwt.encode(
        data_to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return jwt_token
    
def verify_token(token: str, credentials_exception):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = decoded_token.get("user_id")
        if not user_id:
            raise credentials_exception
        
        token_data = TokenData(id = user_id)
        return token_data
    
    except JWTError:
        raise credentials_exception
    
def validate_user(token: str = Depends(oaut2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                          detail="Could not find token",
                                          headers={"WWW_Authenticate": "Bearer"})
    
    token = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()
    return user
    


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)