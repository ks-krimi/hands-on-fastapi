from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text

from database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="true")
    rating = Column(Integer, server_default="0")
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("(DATETIME('now'))")
    )
