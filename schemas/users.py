from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    password: str
    repeat_password: str


class GetUser(BaseModel):
    username: str
    id: int
