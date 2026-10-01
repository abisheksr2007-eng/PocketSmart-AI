from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    data: dict,
    expires_minutes: Optional[int] = None,
) -> str:
    payload = data.copy()

    expire_minutes = (
        expires_minutes
        if expires_minutes is not None
        else settings.access_token_expire_minutes
    )

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expire_minutes
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )
    except JWTError:
        return None