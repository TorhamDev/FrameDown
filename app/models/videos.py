from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.users import User


class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="videos")
    qualities: List["VideoQuality"] | None = Relationship(back_populates="video")
    file: str


class VideoQuality(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quality: str
    file: str
    video_id: Optional[int] = Field(default=None, foreign_key="video.id")
    video: Optional["Video"] = Relationship(back_populates="qualities")
