from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.db import get_session
from app.repository.user import UserRepository
from app.schemas.jwt import JwtToken
from app.schemas.users import CreateUser, GetUser, LoginUser
from app.service.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
def create_user(
    user: CreateUser,
    session: Annotated[Session, Depends(get_session)],
) -> GetUser:
    service = UserService(repository=UserRepository(session=session))
    db_user = service.register(username=user.username, password=user.password)

    assert db_user.id is not None

    return GetUser(
        id=db_user.id,
        username=db_user.username,
    )


@router.post("/login")
def login(
    user: LoginUser,
    session: Annotated[Session, Depends(get_session)],
) -> JwtToken:
    service = UserService(repository=UserRepository(session=session))
    return service.login(username=user.username, password=user.password)
