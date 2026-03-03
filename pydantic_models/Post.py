from fastapi import FastAPI,Depends,APIRouter,HTTPException
from pydantic import BaseModel
from Enum import Role
from datetime import datetime
from sqlalchemy.orm import Session
from database_connection import SessionLocal,get_db
from database_models import Post
from database_models import User
from typing import List,Optional

router=APIRouter()

#BaseModel
class PostBase(BaseModel):
    content:str
    likes:int
    dislikes:int

#For Creating the Post Model
class PostCreate(PostBase):
    user_id:int

#For reading the post Model
class PostRead(PostBase):
    id:int
    content:str
    likes:int
    dislikes:int
    created_at:datetime
    updated_at:datetime

class PostUpdate(BaseModel):
    content:Optional[str]=None
    likes:Optional[int]=None
    dislikes:Optional[int]=None
    user_id:Optional[int]=None    #lateer should change

@router.get("/posts/",response_model=List[PostRead]) 
def read_posts(db:Session=Depends(get_db)) :
    posts_db=db.query(Post).all()
    return posts_db


@router.post("/posts/{post_id}",response_model=PostRead)
def post_create(post:PostCreate,db:Session=Depends(get_db)):
    #check if user exists
    db_user=db.query(User).filter(User.id==post.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found")
    
    #create post
    db_posts=Post(content=post.content,
                  likes=post.likes,
                  dislikes=post.dislikes,
                  user_id=post.user_id)  #later get from JWT authentication. for now explicitly provided from JSON 
    db.add(db_posts)
    db.commit()
    db.refresh(db_posts)
    return db_posts


@router.patch("/posts/{post_id}")
def update_post(post_id:int,post:PostUpdate,db:Session=Depends(get_db)):
    db_posts=db.query(Post).filter(Post.id==post_id).first()
    if not db_posts:
        raise HTTPException(status_code=404,detail="post not found")
    else:
        update_data=post.dict(exclude_unset=True)
        for key,value in update_data.items():
            setattr(db_posts,key,value)

        db.commit()
        db.refresh(db_posts)
        return db_posts
    

@router.delete("/posts/{post_id}")
def delete_post(post_id:int,db:Session=Depends(get_db)):
    db_posts=db.query(Post).filter(Post.id==post_id).first()
    if not db_posts:
        raise HTTPException(status_code=404,detail="post not found")
    else:
        db.delete(db_posts)
        db.commit()
        return{"detail":f"Post with {post_id} deleted successfully"}
    
