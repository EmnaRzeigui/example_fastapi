
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool =True


class PostCreate(PostBase):
    pass 

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


    class Config:
         orm_mode= True



class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    


    class Config:
         orm_mode= True



class PostOut(PostBase):
    post: Post
    votes: int

    


class UserCreate(BaseModel):
    email: EmailStr
    password: str




#the response is going to be a sqlalchemy model and we need pydantic to convert it to a pydantic model  

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]= None


class Vote(BaseModel):
    post_id: int
    dir: int= Field(...,le=1)