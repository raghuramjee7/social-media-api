import random
from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from sqlalchemy.orm import Session
from database import model
from database import connect
from database.pyd_models import Post


app = FastAPI()

# to bind db engine to app
model.Base.metadata.create_all(bind = connect.engine) 

# Add Dependency, we get a connection/session to our database
def get_db():
    db = connect.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# this session should be a part of every route
@app.get("/databasetest")
async def test_db(db: Session = Depends(get_db)): 
    posts = db.query(model.Post).all()
    return {
        "message": posts
    }


@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model = Post)
async def create_post(post: Post, db: Session = Depends(get_db)):

    new_post = model.Post(
        title = post.title, 
        id = post.id, 
        content = post.content,
        #published = post.published
        )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.get("/posts", response_model = List[Post])
async def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return posts


@app.get("/posts/{id}")
async def get_posts(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = "Post Not Found"
            )
    
    return {
        "message": "success",
        "data": post
    }

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(model.Post).filter(model.Post.id == id)

    if post.first()==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Post does not exist")

    post.delete(synchronize_session=False)
    db.commit()

@app.put("/posts/{id}")
async def update_post(id: int, post: Post, db: Session = Depends(get_db)):

    post_query = db.query(model.Post).filter(model.Post.id == id)

    if post_query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post Not Found")

    post_query.update(
        post.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return {
        "message": "Success"
    }