from typing import Optional
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

import model
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

data = []


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0


app = FastAPI()


@app.get("/")
def root():
    return {"hello": "world"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return db.query(model.Post).all()


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = model.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    return post


def find_post_index(id: str):
    for index, post in enumerate(data):
        if post.id == id:
            return index


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_post(id: UUID):
    found_index = find_post_index(id)
    if found_index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    data.pop(found_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: UUID, post: Post):
    found_index = find_post_index(id)
    if found_index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )

    post.id = id  # set id with the params id
    data[found_index] = post

    return data[found_index]
