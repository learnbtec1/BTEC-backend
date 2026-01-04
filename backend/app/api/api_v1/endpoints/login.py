from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep, get_current_user
from app.core import security
from app.core.config import settings
from app.crud import authenticate, create_user, get_user_by_email
from app.models import Token, User, UserCreate, UserPublic, UserRegister

router = APIRouter()


@router.post("/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests.
    Username field should contain the user's email address.
    """
    user = authenticate(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post("/register", response_model=UserPublic)
def register_user(
    session: SessionDep,
    user_in: UserRegister,
) -> User:
    """
    Register a new user (development only - no email verification).
    """
    # Check if user already exists
    user = get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )
    
    # Create new user
    user_create = UserCreate(
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
    )
    user = create_user(session=session, user_create=user_create)
    return user


@router.post("/test-token", response_model=UserPublic)
def test_token(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Test access token validity.
    """
    return current_user
