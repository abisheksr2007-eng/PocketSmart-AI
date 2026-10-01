from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user_optional
from ..models import User
from ..schemas import (
    LoginRequest,
    RegisterRequest,
    SessionInfo,
    TokenResponse,
)
from ..security import (
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter(
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=TokenResponse,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(
        User.email == data.email.lower()
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email is already registered.",
        )

    user = User(
        name=data.name.strip(),
        email=data.email.lower(),
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(
        {"sub": str(user.id)}
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == data.email.lower()
    ).first()

    if not user or not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    token = create_access_token(
        {"sub": str(user.id)}
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )


@router.post("/token")
def token_login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    return login(data, db)


@router.post("/logout")
def logout():
    return {
        "success": True,
        "message": (
            "Logout requested. Remove the stored JWT "
            "from the browser/client."
        ),
    }


@router.get(
    "/session-info",
    response_model=SessionInfo,
)
def session_info(
    user: User | None = Depends(
        get_current_user_optional
    ),
):
    if user is None:
        return SessionInfo(
            authenticated=False,
            user=None,
        )

    return SessionInfo(
        authenticated=True,
        user={
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    )


@router.get("/session-data")
def session_data(
    user: User | None = Depends(
        get_current_user_optional
    ),
):
    if user is None:
        return {
            "authenticated": False,
            "user": None,
        }

    return {
        "authenticated": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }