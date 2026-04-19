from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import UserAlreadyExistsException
from app.models.users import User

if TYPE_CHECKING:
    from sqlmodel import Session


class UserRepository:
    def __init__(self, session: "Session") -> None:
        self.session = session

    def create_user(self, username: str, password: str) -> User:
        db_user = User(
            Username=username,
            password=password,
        )
        try:
            self.session.add(db_user)
            self.session.commit()
            self.session.refresh(db_user)
        except IntegrityError:
            self.session.rollback()
            raise UserAlreadyExistsException

        assert db_user.id is not None

        return db_user
