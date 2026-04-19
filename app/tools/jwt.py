from datetime import datetime, timedelta, timezone

import jwt

from app.schemas.jwt import JwtToken


class JWTHandler:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, username: str) -> JwtToken:
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "iat": datetime.now(timezone.utc),
            "username": username,
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return JwtToken(token=token, token_type="bearer")

    def verify_token(self, token: str) -> dict:
        try:
            data = jwt.decode(
                token,
                key=self.secret_key,
                algorithms=[self.algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

        return data
