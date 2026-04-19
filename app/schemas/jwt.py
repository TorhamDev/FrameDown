from pydantic import BaseModel


class JwtToken(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    exp: int
    iat: int
