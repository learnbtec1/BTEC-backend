import os
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models_files import UserFile, UserFilePublic, UserFilesPublic

router = APIRouter()

# Base upload directory
UPLOAD_DIR = Path("/home/runner/work/BTEC-backend/BTEC-backend/uploads")


def get_user_upload_dir(user_id: uuid.UUID) -> Path:
    """Get the upload directory for a specific user."""
    user_dir = UPLOAD_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


@router.post("/upload", response_model=UserFilePublic)
async def upload_file(
    file: UploadFile,
    session: SessionDep,
    current_user: CurrentUser,
) -> UserFile:
    """
    Upload a file for the current user.
    
    Files are stored in uploads/{user_id}/ with a UUID filename.
    Metadata is saved in the database.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Generate unique filename
    file_id = uuid.uuid4()
    file_extension = Path(file.filename).suffix
    stored_filename = f"{file_id}{file_extension}"
    
    # Get user's upload directory
    user_dir = get_user_upload_dir(current_user.id)
    file_path = user_dir / stored_filename
    
    # Save file to disk
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        file_size = len(content)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to save file: {str(e)}"
        )
    
    # Create database record
    db_file = UserFile(
        id=file_id,
        owner_id=current_user.id,
        original_filename=file.filename,
        stored_path=str(file_path),
        content_type=file.content_type or "application/octet-stream",
        size=file_size,
    )
    
    session.add(db_file)
    session.commit()
    session.refresh(db_file)
    
    return db_file


@router.get("/", response_model=UserFilesPublic)
def list_files(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List all files for the current user.
    """
    statement = (
        select(UserFile)
        .where(UserFile.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    files = session.exec(statement).all()
    
    count_statement = select(UserFile).where(UserFile.owner_id == current_user.id)
    count = len(session.exec(count_statement).all())
    
    return UserFilesPublic(data=files, count=count)


@router.get("/{file_id}")
def download_file(
    file_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> FileResponse:
    """
    Download a specific file.
    
    Only the file owner can download the file.
    """
    db_file = session.get(UserFile, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check ownership
    if db_file.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this file"
        )
    
    # Check if file exists on disk
    if not os.path.exists(db_file.stored_path):
        raise HTTPException(
            status_code=404, detail="File not found on disk"
        )
    
    return FileResponse(
        path=db_file.stored_path,
        filename=db_file.original_filename,
        media_type=db_file.content_type,
    )


@router.delete("/{file_id}")
def delete_file(
    file_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> dict[str, str]:
    """
    Delete a specific file.
    
    Only the file owner can delete the file.
    """
    db_file = session.get(UserFile, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check ownership
    if db_file.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this file"
        )
    
    # Delete from disk
    try:
        if os.path.exists(db_file.stored_path):
            os.remove(db_file.stored_path)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete file from disk: {str(e)}"
        )
    
    # Delete from database
    session.delete(db_file)
    session.commit()
    
    return {"message": "File deleted successfully"}
