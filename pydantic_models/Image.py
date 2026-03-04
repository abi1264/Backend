from fastapi import FastAPI,APIRouter,Depends,HTTPException
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from database_connection import SessionLocal,get_db
from typing import Optional,List
from database_models import Image 



#Base Model
class ImageBase(BaseModel):
    imageUrl:str

class ImageCreate(ImageBase):
    post_id:int
    comment_id:int
    

class ImageRead(ImageBase):
    post_id:int
    comment_id:int
    created_at:datetime
    updated_at:datetime

class ImageUpdate(BaseModel):
    imageUrl:Optional[str]=None 
    post_id:Optional[int]=None
    comment_id:Optional[int]=None
    

router=APIRouter()
#HTTP methods

#get methd
@router.get("/images/",response_model=List[ImageRead])
def get_image(db:Session=Depends(get_db)):
    db_image=db.query(Image).all()
    return db_image

@router.get("/images/{image_id}",response_model=ImageRead)
def get_image_by_id(image_id:int,db:Session=Depends(get_db)):
    db_image=db.query(Image).filter(Image.id==image_id).first()
    if not db_image:
        raise HTTPException(status_code=404,detail="Image not found")
    else:
        return db_image
    

#post method
@router.post("/images/",response_model=ImageRead)    
def create_image(image:ImageCreate,db:Session=Depends(get_db)):
    db_image=Image(
        imageUrl=image.imageUrl,
        post_id=image.post_id,
        comment_id=image.comment_id
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


#patch method

@router.patch("/images/{image_id}",response_model=ImageRead)   
def update_image(image_id:int,image:ImageUpdate,db:Session=Depends(get_db)):
    db_image=db.query(Image).filter(Image.id==image_id).first()
    if not db_image:
        raise HTTPException(status_code=404,detail="Image not found")
    else:
        update_data=image.dict(exclude_unset=True)
        for key,value in update_data.items():
            setattr(db_image,key,value)
            db.commit()
            db.refresh(db_image)
            return (db_image)
        

@router.delete("/images/{image_id}")
def delete_image(image_id:int,db:Session=Depends(get_db)):
    db_image=db.query(Image).filter(Image.id==image_id).first()
    if not db_image:
        raise HTTPException(status_code=404,detail="Image not found")
    else:
        db.delete(db_image)
        db.commit()
     
        return{"detail":f"Image with {image_id} is deleted successfully"}
    


    

