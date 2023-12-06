from fastapi import FastAPI
from database import model, connect
from routers import post, user, auth, vote

from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # allow all http methods
    allow_headers=["*"], # allow all http headers
)

# to bind db engine to app
model.Base.metadata.create_all(bind = connect.engine) 

# Add Dependency, we get a connection/session to our database
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)