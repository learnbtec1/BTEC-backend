import sys
import types
from collections.abc import Generator

# Mock whisper module before any other imports
whisper = types.ModuleType('whisper')
whisper.load_model = lambda x: None
sys.modules['whisper'] = whisper

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, create_engine

from app.core.config import settings
from app.main import app
from app.models import Item, User, StudentProgress, SQLModel
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import get_superuser_token_headers

# Use SQLite for testing
test_engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})

# Create all tables
SQLModel.metadata.create_all(test_engine)


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(test_engine) as session:
        # Create superuser
        from app import crud
        from app.models import UserCreate
        from sqlmodel import select
        
        user = session.exec(
            select(User).where(User.email == settings.FIRST_SUPERUSER)
        ).first()
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            user = crud.create_user(session=session, user_create=user_in)
        
        yield session
        
        # Cleanup
        statement = delete(StudentProgress)
        session.execute(statement)
        statement = delete(Item)
        session.execute(statement)
        statement = delete(User)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
