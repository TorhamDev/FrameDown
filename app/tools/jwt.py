from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Header, HTTPException

from app.schemas.jwt import JwtToken, TokenData


class JWTHandler:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, user_id: int) -> JwtToken:
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "iat": datetime.now(timezone.utc),
            "user_id": user_id,
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return JwtToken(token=token, token_type="bearer")

    def verify_token(self, token: str) -> TokenData:
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

        return TokenData(**data)


# NOTE: In a real application, you would want to handle exceptions more gracefully and not expose internal error messages to the client. You might also want to log these errors for debugging purposes.
# NOTE: HTTPBearer is used because openapi-generator does not support custom authentication schemes, and HTTPBearer is a common choice for token-based authentication.
def credentials(httpbearer: Annotated[str | None, Header()] = None) -> TokenData:
    jwt_handler = JWTHandler(
        secret_key="your_secret_key", algorithm="HS256"
    )  # TODO: take values from env variables

    if httpbearer is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        data = jwt_handler.verify_token(token=httpbearer)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    return data
