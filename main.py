from fastapi import Body, FastAPI


app = FastAPI()


@app.get("/")
def root():
    return {"hello": "world"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


@app.post("/posts")
def create_post(payload: dict = Body(...)):
    return {"data": payload["title"]}
