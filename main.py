from fastapi import FastAPI
from database_connection import engine,Base
from pydantic_models import User
from pydantic_models import Post
from pydantic_models import Comment
from pydantic_models import Image



app=FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(User.router)
app.include_router(Post.router)
app.include_router(Comment.router)
app.include_router(Image.router)