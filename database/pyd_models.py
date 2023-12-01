from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    id: int
    title: str
    content: str

class PostCreate(PostBase):
    pass
    class Config:
        from_attributes = True

class User(BaseModel):
    email: EmailStr

class PostReturn(PostBase):
    owner: User

class PostUpdate(BaseModel):
    title: str
    content: str

class UserCreate(BaseModel):
    #id: int
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None