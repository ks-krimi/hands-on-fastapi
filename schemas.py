from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


# class used for response model
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# there are a schema used for user's endpoints

class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    pass


# schema for access token
class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    id: Union[str, None] = None
