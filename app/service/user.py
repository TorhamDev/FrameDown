from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.repository.user import UserRepository


class UserService:
    def __init__(self, repository: "UserRepository") -> None:
        self.repository = repository

    def create_user(self, username: str, password: str):
        return self.repository.create_user(username=username, password=password)
