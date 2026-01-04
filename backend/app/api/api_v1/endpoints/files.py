import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models_files import UserFile, UserFilePublic, UserFilesPublic

router = APIRouter()

# Base upload directory
UPLOAD_BASE_DIR = Path("uploads")
UPLOAD_BASE_DIR.mkdir(exist_ok=True)


@router.post("/upload", response_model=UserFilePublic)
async def upload_file(
    session: SessionDep,
    current_user: CurrentUser,
    file: UploadFile = File(...),
):
    """
    Upload a file and store it locally.
    """
    # Create user-specific directory
    user_dir = UPLOAD_BASE_DIR / str(current_user.id)
    user_dir.mkdir(exist_ok=True)

    # Generate unique filename to avoid conflicts
    file_extension = Path(file.filename or "").suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = user_dir / unique_filename

    # Save file to disk
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Create database record
    db_file = UserFile(
        owner_id=current_user.id,
        filename=file.filename or unique_filename,
        stored_path=str(file_path),
        content_type=file.content_type,
    )
    session.add(db_file)
    session.commit()
    session.refresh(db_file)

    return db_file


@router.get("", response_model=UserFilesPublic)
def list_files(
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    List all files for the current user.
    """
    statement = select(UserFile).where(UserFile.owner_id == current_user.id)
    files = session.exec(statement).all()
    return UserFilesPublic(data=files, count=len(files))


@router.get("/{file_id}")
def download_file(
    file_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    Download a file by ID (with ownership check).
    """
    db_file = session.get(UserFile, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    # Check ownership
    if db_file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this file")

    # Check if file exists on disk
    if not os.path.exists(db_file.stored_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=db_file.stored_path,
        filename=db_file.filename,
        media_type=db_file.content_type or "application/octet-stream",
    )


@router.delete("/{file_id}")
def delete_file(
    file_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    Delete a file (removes both database record and disk file).
    """
    db_file = session.get(UserFile, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    # Check ownership
    if db_file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this file")

    # Delete from disk
    if os.path.exists(db_file.stored_path):
        os.remove(db_file.stored_path)

    # Delete from database
    session.delete(db_file)
    session.commit()

    return {"message": "File deleted successfully"}
