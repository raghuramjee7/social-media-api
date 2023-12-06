from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint

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


class VoteIn(BaseModel):
    id: int
    direction: conint(le=1)
    
class VoteOut(BaseModel):
    post: PostReturn
    user: User