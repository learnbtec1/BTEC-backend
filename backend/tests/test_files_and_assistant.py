"""
Integration tests for Keitagorus files and assistant endpoints.

Tests cover:
- User registration and authentication
- File upload, list, download, and delete operations
- Assistant query functionality
"""
import io
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, select
from sqlmodel.pool import StaticPool

from app.core.config import settings
from app.main import app
from app.models import User
from app.models_files import UserFile
from app.models_progress import StudentProgress


# Create in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Import all models to ensure they're registered
    from app.models import User, Item  # noqa: F401
    from app.models_files import UserFile  # noqa: F401
    from app.models_progress import StudentProgress  # noqa: F401
    
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> TestClient:
    """Create a test client with dependency overrides."""
    from app.api.deps import get_db
    
    def get_db_override():
        yield session
    
    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestAuthenticationFlow:
    """Test user registration and login."""
    
    def test_register_user(self, client: TestClient, session: Session):
        """Test user registration."""
        response = client.post(
            f"{settings.API_V1_STR}/login/register",
            json={
                "email": "testuser@example.com",
                "password": "testpassword123",
                "full_name": "Test User",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "testuser@example.com"
        assert data["full_name"] == "Test User"
        assert "id" in data
    
    def test_register_duplicate_user(self, client: TestClient):
        """Test that duplicate email registration fails."""
        user_data = {
            "email": "duplicate@example.com",
            "password": "password123",
            "full_name": "Duplicate User",
        }
        
        # First registration should succeed
        response1 = client.post(
            f"{settings.API_V1_STR}/login/register",
            json=user_data,
        )
        assert response1.status_code == 200
        
        # Second registration should fail
        response2 = client.post(
            f"{settings.API_V1_STR}/login/register",
            json=user_data,
        )
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"]
    
    def test_login_access_token(self, client: TestClient):
        """Test getting access token via login."""
        # First register a user
        client.post(
            f"{settings.API_V1_STR}/login/register",
            json={
                "email": "logintest@example.com",
                "password": "loginpass123",
                "full_name": "Login Test",
            },
        )
        
        # Then try to login
        response = client.post(
            f"{settings.API_V1_STR}/login/access-token",
            data={
                "username": "logintest@example.com",
                "password": "loginpass123",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client: TestClient):
        """Test login with incorrect password."""
        # Register user
        client.post(
            f"{settings.API_V1_STR}/login/register",
            json={
                "email": "wrongpass@example.com",
                "password": "correctpass",
                "full_name": "Wrong Pass",
            },
        )
        
        # Try to login with wrong password
        response = client.post(
            f"{settings.API_V1_STR}/login/access-token",
            data={
                "username": "wrongpass@example.com",
                "password": "wrongpassword",
            },
        )
        
        assert response.status_code == 400
        assert "Incorrect email or password" in response.json()["detail"]


class TestFileOperations:
    """Test file upload, list, download, and delete operations."""
    
    @pytest.fixture
    def auth_headers(self, client: TestClient) -> dict[str, str]:
        """Create a user and return authentication headers."""
        # Register user
        client.post(
            f"{settings.API_V1_STR}/login/register",
            json={
                "email": "fileuser@example.com",
                "password": "filepass123",
                "full_name": "File User",
            },
        )
        
        # Login to get token
        response = client.post(
            f"{settings.API_V1_STR}/login/access-token",
            data={
                "username": "fileuser@example.com",
                "password": "filepass123",
            },
        )
        
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_upload_file(self, client: TestClient, auth_headers: dict[str, str]):
        """Test file upload."""
        file_content = b"This is a test file content"
        file = io.BytesIO(file_content)
        
        response = client.post(
            f"{settings.API_V1_STR}/files/upload",
            headers=auth_headers,
            files={"file": ("test_file.txt", file, "text/plain")},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["original_filename"] == "test_file.txt"
        assert data["content_type"] == "text/plain"
        assert data["size"] == len(file_content)
        assert "id" in data
    
    def test_list_files(self, client: TestClient, auth_headers: dict[str, str]):
        """Test listing files."""
        # Upload a few files first
        for i in range(3):
            file = io.BytesIO(f"File content {i}".encode())
            client.post(
                f"{settings.API_V1_STR}/files/upload",
                headers=auth_headers,
                files={"file": (f"file_{i}.txt", file, "text/plain")},
            )
        
        # List files
        response = client.get(
            f"{settings.API_V1_STR}/files/",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "count" in data
        assert data["count"] >= 3
        assert len(data["data"]) >= 3
    
    def test_download_file(self, client: TestClient, auth_headers: dict[str, str]):
        """Test file download."""
        # Upload a file
        file_content = b"Download test content"
        file = io.BytesIO(file_content)
        
        upload_response = client.post(
            f"{settings.API_V1_STR}/files/upload",
            headers=auth_headers,
            files={"file": ("download_test.txt", file, "text/plain")},
        )
        
        file_id = upload_response.json()["id"]
        
        # Download the file
        response = client.get(
            f"{settings.API_V1_STR}/files/{file_id}",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        assert response.content == file_content
    
    def test_delete_file(self, client: TestClient, auth_headers: dict[str, str], session: Session):
        """Test file deletion."""
        # Upload a file
        file = io.BytesIO(b"Delete test content")
        
        upload_response = client.post(
            f"{settings.API_V1_STR}/files/upload",
            headers=auth_headers,
            files={"file": ("delete_test.txt", file, "text/plain")},
        )
        
        file_id = upload_response.json()["id"]
        
        # Delete the file
        response = client.delete(
            f"{settings.API_V1_STR}/files/{file_id}",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
        
        # Verify file is deleted from database
        db_file = session.get(UserFile, file_id)
        assert db_file is None
    
    def test_unauthorized_file_access(self, client: TestClient):
        """Test that unauthorized users cannot access files."""
        response = client.get(f"{settings.API_V1_STR}/files/")
        assert response.status_code == 401


class TestAssistant:
    """Test AI assistant query functionality."""
    
    @pytest.fixture
    def auth_headers(self, client: TestClient, session: Session) -> dict[str, str]:
        """Create a user with progress data and return authentication headers."""
        # Register user
        register_response = client.post(
            f"{settings.API_V1_STR}/login/register",
            json={
                "email": "assistant@example.com",
                "password": "assistpass123",
                "full_name": "Assistant User",
            },
        )
        
        user_id = register_response.json()["id"]
        
        # Create some progress records
        from app.models_progress import StudentProgress
        import uuid
        from datetime import datetime, timezone
        
        progress1 = StudentProgress(
            user_id=uuid.UUID(user_id),
            lesson_id=uuid.uuid4(),
            progress_percentage=75,
            last_score=72.5,
            attempts=2,
            struggling=False,
        )
        progress2 = StudentProgress(
            user_id=uuid.UUID(user_id),
            lesson_id=uuid.uuid4(),
            progress_percentage=40,
            last_score=55.0,
            attempts=5,
            struggling=True,
        )
        
        session.add(progress1)
        session.add(progress2)
        session.commit()
        
        # Login to get token
        response = client.post(
            f"{settings.API_V1_STR}/login/access-token",
            data={
                "username": "assistant@example.com",
                "password": "assistpass123",
            },
        )
        
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_assistant_query_help(self, client: TestClient, auth_headers: dict[str, str]):
        """Test assistant query with 'help' keyword."""
        response = client.post(
            f"{settings.API_V1_STR}/assistant/query",
            headers=auth_headers,
            json={
                "prompt": "I need help with my studies",
                "context": None,
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "recommendations" in data
        assert "actions" in data
        assert "Keitagorus" in data["answer"]
        assert len(data["recommendations"]) > 0
    
    def test_assistant_query_progress(self, client: TestClient, auth_headers: dict[str, str]):
        """Test assistant query about progress."""
        response = client.post(
            f"{settings.API_V1_STR}/assistant/query",
            headers=auth_headers,
            json={
                "prompt": "Show me my progress",
                "context": None,
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "2 lesson(s)" in data["answer"]
        assert "struggling" in data["answer"]
        assert len(data["recommendations"]) > 0
        assert "view_detailed_progress" in data["actions"]
    
    def test_assistant_query_study(self, client: TestClient, auth_headers: dict[str, str]):
        """Test assistant query about study recommendations."""
        response = client.post(
            f"{settings.API_V1_STR}/assistant/query",
            headers=auth_headers,
            json={
                "prompt": "Give me study tips",
                "context": None,
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "study" in data["answer"].lower()
        assert len(data["recommendations"]) > 0
    
    def test_assistant_query_with_context(self, client: TestClient, auth_headers: dict[str, str]):
        """Test assistant query with additional context."""
        response = client.post(
            f"{settings.API_V1_STR}/assistant/query",
            headers=auth_headers,
            json={
                "prompt": "I'm having trouble understanding",
                "context": "This topic is very difficult for me",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "recommendations" in data
        # Should include context-aware recommendation
        assert any("step" in rec.lower() for rec in data["recommendations"])
    
    def test_assistant_unauthorized(self, client: TestClient):
        """Test that unauthorized users cannot query assistant."""
        response = client.post(
            f"{settings.API_V1_STR}/assistant/query",
            json={
                "prompt": "Help me",
                "context": None,
            },
        )
        
        assert response.status_code == 401
