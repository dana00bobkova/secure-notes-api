from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.security import create_access_token, hash_password, verify_password
from app.database import get_db
from app.models import User
from app.rate_limit import login_rate_limiter
from app.schemas import Token, UserCreate, UserLogin, UserRead
from app.services.audit_logger import log_audit_event

auth_router = APIRouter()


@auth_router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user is not None:
        log_audit_event(
            db=db,
            event_type="USER_REGISTRATION_FAILED",
            success=False,
            request=request,
            email=user_data.email,
            details="Registration failed because email already exists."
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    log_audit_event(
        db=db,
        event_type="USER_REGISTERED",
        success=True,
        request=request,
        user_id=new_user.id,
        email=new_user.email,
        details="New user account created."
    )

    return new_user


@auth_router.post(
    "/login",
    response_model=Token
)
def login_user(
    login_data: UserLogin,
    request: Request,
    _rate_limit: None = Depends(login_rate_limiter),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if user is None:
        log_audit_event(
            db=db,
            event_type="LOGIN_FAILED",
            success=False,
            request=request,
            email=login_data.email,
            details="Login failed because email was not found."
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not verify_password(login_data.password, user.hashed_password):
        log_audit_event(
            db=db,
            event_type="LOGIN_FAILED",
            success=False,
            request=request,
            user_id=user.id,
            email=user.email,
            details="Login failed because password was incorrect."
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not user.is_active:
        log_audit_event(
            db=db,
            event_type="LOGIN_FAILED",
            success=False,
            request=request,
            user_id=user.id,
            email=user.email,
            details="Login failed because user account is disabled."
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    log_audit_event(
        db=db,
        event_type="LOGIN_SUCCESS",
        success=True,
        request=request,
        user_id=user.id,
        email=user.email,
        details="User logged in successfully."
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"  # nosec B105 - OAuth2 token type label, not a password
    }


@auth_router.get(
    "/me",
    response_model=UserRead
)
def read_current_user(
    current_user: User = Depends(get_current_user)
):
    return current_user
