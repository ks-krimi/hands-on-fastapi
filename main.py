from fastapi import FastAPI

from database import Base, engine
from routers import auth, post, user

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/", tags=["Root"])
def root():
    return {"hello": "world"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
