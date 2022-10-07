from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


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
def get_posts():
    return {"data": "This is your posts"}


@app.post("/posts")
def create_post(post: Post):
    return post.dict()
