from fastapi import FastAPI,Depends,APIRouter,HTTPException
from pydantic import BaseModel
from Enum import Role
from datetime import datetime
from sqlalchemy.orm import Session
from database_connection import SessionLocal,get_db
from database_models import User
from typing import Optional


from typing import List

router=APIRouter()
#Model for sharing 
class UserBase(BaseModel):
    name:str
    role:Role

#Model for Creating User
class UserCreate(UserBase):
    email:str
    password:str

#Model for reading user
class UserRead(UserBase):
    id:int
    email:str
    created_at:datetime
    updated_at:datetime

class UserUpdate(BaseModel):
    name:Optional[str] =None
    role:Optional[Role]=None
    email:Optional[str]=None
    password:Optional[str]=None


@router.get("/users/",response_model=List[UserRead])
def read_user(db:Session=Depends(get_db)):
    user_db=db.query(User).all()
    return user_db


@router.get("/users/{user_id}",response_model=UserRead)
def read_user_by_id(user_id:int,db:Session=Depends(get_db)):
    user_db=db.query(User).filter(User.id==user_id).first()
    if not user_db:
        raise HTTPException(status_code=404,detail="Usr not Found")
    else:
        return user_db


#Create a new user
@router.post("/users/",response_model=UserRead)
def user_create(user:UserCreate, db:Session=Depends(get_db)):
    db_user=User(
        name=user.name,
        role=user.role,
        email=user.email,
        password=user.password
                )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.patch("/users/{user_id}")
def update_user(user_id: int,user:UserUpdate,db:Session=Depends(get_db)):
   db_user=db.query(User).filter(User.id==user_id).first()
   if not db_user:
       raise HTTPException(status_code=404,detail="User not found")
   else:
       update_data=user.dict(exclude_unset=True) #conver user object in dictoionary key : value pair 
       for key,value in update_data.items(): 
           setattr(db_user,key,value)   # it means db_user.age=24. same thing 

       db.commit()
       db.refresh(db_user)
       return db_user        
     


@router.delete("/users/{user_id}")    
def delete_user(user_id:int,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.id==user_id).first()
    if not  db_user:
        raise HTTPException(status_code=404,detail="User not found")
    db.delete(db_user)
    db.commit()
    return{"detail":f"User with id {user_id} deleted successfully"}



