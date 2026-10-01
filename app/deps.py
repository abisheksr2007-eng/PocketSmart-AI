from typing import Optional

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .security import decode_access_token


def get_current_user_optional(
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
) -> Optional[User]:

    if not authorization:
        return None

    if not authorization.lower().startswith("bearer "):
        return None

    token = authorization.split(" ", 1)[1].strip()

    payload = decode_access_token(token)

    if not payload:
        return None

    user_id = payload.get("sub")

    if not user_id:
        return None

    return db.query(User).filter(
        User.id == int(user_id)
    ).first()


def get_current_user(
    user: Optional[User] = Depends(get_current_user_optional),
) -> User:

    if user is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=401,
            detail="Authentication required.",
        )

    return user