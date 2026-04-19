from typing import TYPE_CHECKING

from app.core.exceptions import InvalidCredentialsException
from app.schemas.jwt import JwtToken
from app.tools.jwt import JWTHandler
from app.tools.passwd import pwd_context

if TYPE_CHECKING:
    from app.repository.user import UserRepository


class UserService:
    def __init__(self, repository: "UserRepository") -> None:
        self.repository = repository
        self.jwt_handler = JWTHandler(secret_key="your_secret_key", algorithm="HS256")

    def register(self, username: str, password: str):
        password_hash = pwd_context.hash(password)
        return self.repository.create_user(username=username, password=password_hash)

    def login(self, username: str, password: str) -> JwtToken:
        user = self.repository.get_user_by_username(username=username)

        if user is None:
            raise InvalidCredentialsException

        if not pwd_context.verify(password, user.password):
            raise InvalidCredentialsException

        return self.jwt_handler.create_token(username=username)
