from fastapi import FastAPI,APIRouter,HTTPException,Depends
from pydantic import BaseModel
from Enum import Role
from datetime import datetime
from sqlalchemy.orm import Session
from database_connection import get_db,SessionLocal
from database_models import Comment
from typing import Optional,List

router=APIRouter()

class CommentBase(BaseModel):
    content:str

class CommentCreate(CommentBase):
    user_id:int
    post_id:int  

class CommentRead(CommentBase):
    user_id:int
    post_id:int
    created_at:datetime
    updated_at:datetime

class CommentUpdate(BaseModel):
    content:Optional[str]=None
    user_id:Optional[int]=None
    post_id:Optional[int]=None

#HTTP METHODs

@router.get("/comment/",response_model=List[CommentRead])
def read_comment(db:Session=Depends(get_db)):
    db_comment=db.query(Comment).all()
    return db_comment

#get comment by id
@router.get("/comment/{comment_id}",response_model=CommentRead)
def read_comment_by_id(comment_id:int,db:Session=Depends(get_db)):
    db_comment=db.query(Comment).filter(Comment.id==comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    else:
        return db_comment
    
#post method
@router.post("/comment/",response_model=CommentRead)   
def create_comment(comment:CommentCreate,db:Session=Depends(get_db)):
    db_comment=Comment(
        content=comment.content,
        user_id=comment.user_id,
        post_id=comment.post_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


#patch method
@router.patch("/comment/{comment_id}",response_model=CommentRead)
def update_comment(comment_id:int,comment:CommentUpdate,db:Session=Depends(get_db)):
    db_comment=db.query(Comment).filter(Comment.id==comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    else:
        update_data=comment.dict(exclude_unset=True)
        for key,value in update_data.items():
            setattr(db_comment,key, value)
            db.commit()
            db.refresh(db_comment)
            return db_comment
        
#delete method
@router.delete("/comment/{comment_id}")  
def delete_comment(comment_id:int,db:Session=Depends(get_db)):
    db_comment=db.query(Comment).filter(Comment.id==comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    else:
        db.delete(db_comment)
        db.commit()
        return{"detail":f"Comment with {comment_id} is deleted successfully"}





