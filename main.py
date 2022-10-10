from fastapi import FastAPI

from database import Base, engine
from routers import post, user

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)


@app.get("/", tags=["Root"])
def root():
    return {"hello": "world"}
