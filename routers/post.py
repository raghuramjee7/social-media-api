from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import Session
from database import model
from database.pyd_models import PostCreate, PostReturn, PostUpdate
from database.connect import get_db
from fastapi import APIRouter
from app.utils import validate_user

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = PostCreate)
async def create_post(post: PostCreate, db: Session = Depends(get_db), user: int = Depends(validate_user)):

    new_post = model.Post(
        title = post.title, 
        id = post.id, 
        content = post.content,
        owner_id = user.id
        #published = post.published
        )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/", response_model = List[PostReturn])
async def get_all_posts(db: Session = Depends(get_db), user: int = Depends(validate_user),
                        limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}", response_model = PostReturn)
async def get_posts(id: int, response: Response, db: Session = Depends(get_db), user: int = Depends(validate_user)):
    post = db.query(model.Post).filter(model.Post.id == id).first()

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = "Post Not Found"
            )
    if post.owner_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not Authorised")
    return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), user: int = Depends(validate_user)):

    post = db.query(model.Post).filter(model.Post.id == id)

    if post.first()==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Post does not exist")
    if post.first().owner_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not Authorised")
    post.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}")
async def update_post(id: int, post: PostUpdate, db: Session = Depends(get_db), user: int = Depends(validate_user)):

    post_query = db.query(model.Post).filter(model.Post.id == id)

    if post_query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post Not Found")

    if post_query.first().owner_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not Authorised")
    
    post_query.update(
        post.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return {
        "message": "Success"
    }


