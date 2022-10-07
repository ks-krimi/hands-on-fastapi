from typing import Optional
from uuid import UUID, uuid4

from fastapi import FastAPI
from pydantic import BaseModel

data = []


class Post(BaseModel):
    id: Optional[UUID] = uuid4()
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
    return data


@app.post("/posts")
def create_post(post: Post):
    post.id = uuid4()  # generate new uuid
    data.append(post)
    return post
