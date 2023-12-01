from fastapi import FastAPI
from database import model, connect
from routers import post, user, auth

app = FastAPI()

# to bind db engine to app
model.Base.metadata.create_all(bind = connect.engine) 

# Add Dependency, we get a connection/session to our database
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)