from fastapi.encoders import jsonable_encoder
from app import oauth2
from .. import models, schemas, utils
from fastapi import  FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func



router= APIRouter(
    prefix="/posts" ,
    tags= ['Posts']
)

# @router.get("/", response_model= List[schemas.PostOut])
@router.get("/")
def test_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), Limit: int = 10, skip: int =0, search: Optional[str]= ""  ):
    
    posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    posts_query = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .limit(Limit)
        .offset(skip)
    )

    results = posts_query.all()

    

    return posts
    

@router.get("/{id}", response_model=schemas.Post)
def get_post(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post=  db.query(models.Post).filter(models.Post.id == id).first()
   
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                     detail= f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"not authorized to perfomr requested action")

    
    return post


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #new_post = models.Post(title= post.title, content= post.content, published= post.published )
    new_post= models.Post(owner_id= current_user.id , **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user= Depends(oauth2.get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id == id)
    

    post = post_query.first()
    if  post  == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"not authorized to perfomr requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id == id)
    post= post_query.first()
    
    if post == None:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                     detail= f"post with id: {id} does not exist"                   )
    

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"not authorized to perfomr requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

