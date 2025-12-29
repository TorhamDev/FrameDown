from sqlmodel import SQLModel

from database.db import engine

from .users import User

__all__ = [
    "User",
]

SQLModel.metadata.create_all(
    engine,
    checkfirst=True,
)
