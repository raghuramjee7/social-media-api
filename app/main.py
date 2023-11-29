import random
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

class Post(BaseModel):
    title: str 
    content: str
    published: bool = True
    rating: Optional[int] = None

app = FastAPI()

posts_array = []

@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }

@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_post(post: Post):
    post = post.model_dump()
    post["id"] = random.randint(1,1000000)
    posts_array.append(post)

    return {
        "message": "Post Succesfully Created",
        "data": post
    }

@app.get("/posts")
async def get_all_posts():
    return {
        "data": posts_array
    }


@app.get("/posts/{id}")
async def get_posts(id: int, response: Response):
    for post in posts_array:
        if post['id']==id:
            return {
                "data": post
            }
    # response.status_code = status.HTTP_404_NOT_FOUND 
    # return {
    #     "message": "Post Not Found"
    # }
    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail = "Post Not Found"
        )

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):

    for ind, post in enumerate(posts_array):
        if post['id']==id: 
            posts_array.pop(ind)
            return Response(status_code = status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Post does not exist")

@app.put("/posts/{id}")
async def update_post(id: int, updated_post: Post):
    post_new = updated_post.model_dump()
    for ind, post in enumerate(posts_array):
        if post["id"] == id:
            post_new['id'] = id
            posts_array[ind] = post_new
            return {
                "message": "Post Updated"
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post Not Found")
