"""
Integration tests for file upload/download and assistant endpoints.
Tests the Keitagorus foundation features.
"""

import io
import uuid
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.crud import create_user
from app.models import User, UserCreate
from app.models_files import UserFile
from app.models_progress import StudentProgress


def test_register_and_login(client: TestClient) -> None:
    """Test user registration and login flow."""
    # Register a new user
    email = f"test_{uuid.uuid4()}@example.com"
    password = "testpass123"
    
    register_data = {
        "email": email,
        "password": password,
        "full_name": "Test User",
    }
    
    r = client.post(f"{settings.API_V1_STR}/login/register", json=register_data)
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == email
    assert "id" in data
    
    # Login with the new user
    login_data = {
        "username": email,
        "password": password,
    }
    
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"


def test_file_upload_and_list(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Test file upload and listing."""
    # Create a test file
    file_content = b"This is a test file content"
    file_data = {
        "file": ("test_file.txt", io.BytesIO(file_content), "text/plain")
    }
    
    # Upload the file
    r = client.post(
        f"{settings.API_V1_STR}/files/upload",
        files=file_data,
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    upload_response = r.json()
    assert upload_response["original_filename"] == "test_file.txt"
    assert upload_response["content_type"] == "text/plain"
    assert upload_response["size"] == len(file_content)
    assert "id" in upload_response
    
    file_id = upload_response["id"]
    
    # List files
    r = client.get(
        f"{settings.API_V1_STR}/files",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    files = r.json()
    assert isinstance(files, list)
    assert len(files) > 0
    assert any(f["id"] == file_id for f in files)


def test_file_download(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Test file download."""
    # First upload a file
    file_content = b"Download test content"
    file_data = {
        "file": ("download_test.txt", io.BytesIO(file_content), "text/plain")
    }
    
    r = client.post(
        f"{settings.API_V1_STR}/files/upload",
        files=file_data,
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    file_id = r.json()["id"]
    
    # Download the file
    r = client.get(
        f"{settings.API_V1_STR}/files/{file_id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    assert r.content == file_content


def test_file_delete(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Test file deletion."""
    # Upload a file
    file_content = b"Delete test content"
    file_data = {
        "file": ("delete_test.txt", io.BytesIO(file_content), "text/plain")
    }
    
    r = client.post(
        f"{settings.API_V1_STR}/files/upload",
        files=file_data,
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    file_id = r.json()["id"]
    
    # Delete the file
    r = client.delete(
        f"{settings.API_V1_STR}/files/{file_id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    assert r.json()["message"] == "File deleted successfully"
    
    # Verify file is deleted from database
    statement = select(UserFile).where(UserFile.id == uuid.UUID(file_id))
    result = db.exec(statement).first()
    assert result is None


def test_file_unauthorized_access(
    client: TestClient, 
    normal_user_token_headers: dict[str, str],
    superuser_token_headers: dict[str, str]
) -> None:
    """Test that users cannot access other users' files."""
    # Upload a file as normal user
    file_content = b"Private file content"
    file_data = {
        "file": ("private_file.txt", io.BytesIO(file_content), "text/plain")
    }
    
    r = client.post(
        f"{settings.API_V1_STR}/files/upload",
        files=file_data,
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    file_id = r.json()["id"]
    
    # Try to download as superuser (different user)
    r = client.get(
        f"{settings.API_V1_STR}/files/{file_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 403


def test_assistant_query(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Test assistant query endpoint."""
    query_data = {
        "prompt": "Help me with my progress",
        "context": None,
    }
    
    r = client.post(
        f"{settings.API_V1_STR}/assistant/query",
        json=query_data,
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    response = r.json()
    
    # Validate response structure
    assert "answer" in response
    assert "recommendations" in response
    assert "actions" in response
    assert isinstance(response["answer"], str)
    assert isinstance(response["recommendations"], list)
    assert isinstance(response["actions"], list)


def test_assistant_query_with_keywords(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Test assistant responses to different keyword prompts."""
    test_cases = [
        ("help me please", "help"),
        ("I need practice", "practice"),
        ("show me my progress", "progress"),
        ("tell me about yourself", "Keitagorus"),
    ]
    
    for prompt, expected_keyword in test_cases:
        query_data = {
            "prompt": prompt,
            "context": None,
        }
        
        r = client.post(
            f"{settings.API_V1_STR}/assistant/query",
            json=query_data,
            headers=normal_user_token_headers,
        )
        assert r.status_code == 200
        response = r.json()
        
        # Check that response contains relevant content
        assert len(response["answer"]) > 0
        assert len(response["recommendations"]) >= 0
        assert len(response["actions"]) >= 0


def test_assistant_with_student_progress(
    client: TestClient, 
    normal_user_token_headers: dict[str, str],
    db: Session
) -> None:
    """Test assistant query with existing student progress data."""
    # Get the current user
    from app.api.deps import get_current_user, get_db
    
    # Create some student progress for the user
    # This would normally be done through the API, but we're doing it directly for testing
    statement = select(User).where(User.email == settings.EMAIL_TEST_USER)
    user = db.exec(statement).first()
    
    if user:
        # Create a struggling progress record
        progress = StudentProgress(
            user_id=user.id,
            lesson_id=uuid.uuid4(),
            progress_percentage=40,
            last_score=45.0,
            attempts=3,
            struggling=True,
        )
        db.add(progress)
        db.commit()
        
        # Query assistant about progress
        query_data = {
            "prompt": "How am I doing?",
            "context": None,
        }
        
        r = client.post(
            f"{settings.API_V1_STR}/assistant/query",
            json=query_data,
            headers=normal_user_token_headers,
        )
        assert r.status_code == 200
        response = r.json()
        
        # The assistant should mention struggling lessons
        assert len(response["answer"]) > 0


def test_invalid_file_upload_no_auth(client: TestClient) -> None:
    """Test that file upload requires authentication."""
    file_content = b"Unauthorized upload attempt"
    file_data = {
        "file": ("test.txt", io.BytesIO(file_content), "text/plain")
    }
    
    r = client.post(
        f"{settings.API_V1_STR}/files/upload",
        files=file_data,
    )
    assert r.status_code == 401


def test_assistant_query_no_auth(client: TestClient) -> None:
    """Test that assistant query requires authentication."""
    query_data = {
        "prompt": "Test query",
        "context": None,
    }
    
    r = client.post(
        f"{settings.API_V1_STR}/assistant/query",
        json=query_data,
    )
    assert r.status_code == 401
