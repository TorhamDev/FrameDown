from fastapi import HTTPException


class BaseException(HTTPException):
    status_code = 500
    detail = "An error occurred"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BaseException):
    status_code = 400
    detail = "User with the given username already exists"
