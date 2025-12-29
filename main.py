from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session

from database.db import get_session
from models.users import User
from schemas.users import CreateUser, GetUser

app = FastAPI(debug=True)

# TODO: user lifespan to create database tables


@app.post("/register")
def create_user(
    user: CreateUser,
    session: Annotated[Session, Depends(get_session)],
) -> GetUser:
    db_user = User(
        Username=user.username,
        password=user.password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    assert db_user.id is not None

    return GetUser(
        username=db_user.Username,
        id=db_user.id,
    )
