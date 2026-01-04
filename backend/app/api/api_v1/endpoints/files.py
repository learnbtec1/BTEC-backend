import os
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models_files import UserFile, UserFilePublic

router = APIRouter()

# Base upload directory
UPLOAD_DIR = Path("uploads")


def get_user_upload_dir(user_id: uuid.UUID) -> Path:
    """Get or create upload directory for a specific user."""
    user_dir = UPLOAD_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


@router.post("/upload", response_model=UserFilePublic)
async def upload_file(
    session: SessionDep,
    current_user: CurrentUser,
    file: Annotated[UploadFile, File()],
) -> UserFile:
    """
    Upload a file for the current user.
    Files are stored in uploads/{user_id}/ with a UUID filename.
    """
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Get user's upload directory
    user_dir = get_user_upload_dir(current_user.id)
    file_path = user_dir / unique_filename
    
    # Save file to disk
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # Create database record
    db_file = UserFile(
        owner_id=current_user.id,
        original_filename=file.filename,
        stored_path=str(file_path),
        content_type=file.content_type or "application/octet-stream",
        size=len(contents),
    )
    
    session.add(db_file)
    session.commit()
    session.refresh(db_file)
    
    return db_file


@router.get("", response_model=list[UserFilePublic])
def list_files(
    session: SessionDep,
    current_user: CurrentUser,
) -> list[UserFile]:
    """
    List all files for the current user.
    """
    statement = select(UserFile).where(UserFile.owner_id == current_user.id)
    files = session.exec(statement).all()
    return list(files)


@router.get("/{file_id}")
def download_file(
    session: SessionDep,
    current_user: CurrentUser,
    file_id: uuid.UUID,
) -> FileResponse:
    """
    Download a specific file by ID.
    Only the file owner can download the file.
    """
    # Get file metadata
    db_file = session.get(UserFile, file_id)
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check ownership
    if db_file.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this file"
        )
    
    # Check if file exists on disk
    if not os.path.exists(db_file.stored_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk"
        )
    
    return FileResponse(
        path=db_file.stored_path,
        filename=db_file.original_filename,
        media_type=db_file.content_type,
    )


@router.delete("/{file_id}")
def delete_file(
    session: SessionDep,
    current_user: CurrentUser,
    file_id: uuid.UUID,
) -> dict[str, str]:
    """
    Delete a file by ID.
    Only the file owner can delete the file.
    """
    # Get file metadata
    db_file = session.get(UserFile, file_id)
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check ownership
    if db_file.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this file"
        )
    
    # Delete file from disk
    try:
        if os.path.exists(db_file.stored_path):
            os.remove(db_file.stored_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file from disk: {str(e)}"
        )
    
    # Delete database record
    session.delete(db_file)
    session.commit()
    
    return {"message": "File deleted successfully"}
