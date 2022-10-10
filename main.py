from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

import model
from database import Base, engine, get_db
from schemas import Post, PostCreate, PostUpdate

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def root():
    return {"hello": "world"}


@app.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    return db.query(model.Post).all()


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = model.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=Post)
def update_post(id: int, post: PostUpdate, db: Session = Depends(get_db)):
    query = db.query(model.Post).filter(model.Post.id == id)
    if query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    return query.first()
