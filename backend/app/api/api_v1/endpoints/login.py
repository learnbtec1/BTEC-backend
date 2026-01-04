from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import SessionDep, get_current_user
from app.core import security
from app.core.config import settings
from app.models import Token, UserPublic, UserCreate, User

router = APIRouter()


@router.post("/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests.
    
    Username field should contain the user's email address.
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token)


@router.post("/register", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserCreate) -> User:
    """
    Register a new user (development only - no email verification).
    
    WARNING: This endpoint is for development purposes only.
    In production, implement proper email verification and rate limiting.
    """
    # Check if user already exists
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists in the system",
        )
    
    # Create new user
    user = crud.create_user(session=session, user_create=user_in)
    return user
