from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="true")
    rating = Column(Integer, server_default="0")
