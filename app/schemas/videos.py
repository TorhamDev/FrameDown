from pydantic import BaseModel


class Video(BaseModel):
    id: int
    title: str
    user_id: int
    file: str
