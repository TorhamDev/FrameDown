from pydantic import BaseModel


class JwtToken(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    exp: int
    iat: int
