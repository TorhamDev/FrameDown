from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.videos import Video


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str

    videos: List["Video"] = Relationship(back_populates="user")
