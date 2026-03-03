from fastapi import FastAPI
from database_connection import Base
from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime
from Enum import Role
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


app=FastAPI()

class User(Base):
    __tablename__="User"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(255),index=True)
    email=Column(String(255),index=True)
    password=Column(String(255),index=True)
    role=Column(
        ENUM(Role,name="Role_enum"),nullable=False)
    
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    #Relationship
    posts=relationship("Post",back_populates="user")
    comments=relationship("Comment",back_populates="user")


    


# next class

class Post(Base):
    __tablename__="Post"
    id=Column(Integer,primary_key=True,index=True)
    content=Column(String(500),index=True)
    likes=Column(Integer,index=True)
    dislikes=Column(Integer,index=True)
    user_id=Column(Integer,ForeignKey("User.id"),nullable=False,index=True)  #Foreign key

    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    #Relationship
    user=relationship("User",back_populates="posts")  #one to many
    image=relationship("Image",back_populates="post")  #one to one
    comments=relationship("Comment",back_populates="post")  #one to many



# next class
class Comment(Base):
    __tablename__="Comment"
    id=Column(Integer,primary_key=True,index=True)
    content=Column(String(500),index=True)
    user_id=Column(ForeignKey("User.id"),nullable=False,index=True)
    post_id=Column(ForeignKey("Post.id"),nullable=False,index=True)
    
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    user=relationship("User",back_populates="comments")
    post=relationship("Post",back_populates="comments")
    images=relationship("Image",back_populates="comments")




#next class
class Image(Base):
    __tablename__="Image"
    id=Column(Integer,primary_key=True,index=True)
    imageUrl=Column(String(255),index=True)

    post_id=Column(ForeignKey("Post.id"),nullable=False,index=True)

    comment_id=Column(ForeignKey("Comment.id"),nullable=False,index=True)

    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    #RelationShip
    post=relationship("Post",back_populates="image")
    comments=relationship("Comment",back_populates="images")






    

