from typing import Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, Response, status
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


def find_post(id: str):
    for post in data:
        if post.id == id:
            return post


@app.get("/posts/{id}")
def get_post(id: UUID, response: Response):
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Post with id {id} is not found"}
    return post
