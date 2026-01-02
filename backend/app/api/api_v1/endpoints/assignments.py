import os
import uuid
from typing import Any
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session

from app import crud
from app.api.deps import CurrentUser, SessionDep, TeacherUser, StudentUser
from app.models import (
    Assignment,
    AssignmentCreate,
    AssignmentPublic,
    AssignmentsPublic,
    AssignmentStats,
    AssignmentUpdate,
    Message,
)

router = APIRouter()

# File upload configuration
UPLOAD_DIR = Path("/home/runner/work/BTEC-backend/BTEC-backend/backend/uploads/assignments")
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".zip", ".jpg", ".jpeg", ".png", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_file(file: UploadFile) -> None:
    """Validate file type and size"""
    # Check file extension
    file_ext = os.path.splitext(file.filename or "")[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}",
        )


def save_upload_file(file: UploadFile) -> tuple[str, str, int]:
    """Save uploaded file and return (file_path, original_name, file_size)"""
    # Create upload directory if it doesn't exist
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename or "")[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    file_size = 0
    with open(file_path, "wb") as f:
        content = file.file.read()
        file_size = len(content)
        
        # Check file size
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024 * 1024):.1f} MB",
            )
        
        f.write(content)
    
    return str(file_path), file.filename or unique_filename, file_size


@router.post("/upload", response_model=AssignmentPublic)
def upload_assignment(
    *,
    session: SessionDep,
    current_user: StudentUser,
    title: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
) -> Any:
    """
    Upload a new assignment (students only).
    """
    # Validate file
    validate_file(file)
    
    # Save file
    file_path, file_name, file_size = save_upload_file(file)
    
    # Create assignment record
    assignment_in = AssignmentCreate(title=title, description=description)
    assignment = crud.create_assignment(
        session=session,
        assignment_in=assignment_in,
        student_id=current_user.id,
        file_path=file_path,
        file_name=file_name,
        file_size=file_size,
    )
    
    return assignment


@router.get("/my", response_model=AssignmentsPublic)
def get_my_assignments(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get assignments for the current user.
    Students see their own assignments, teachers see all assignments.
    """
    if current_user.role == "teacher" or current_user.is_superuser:
        # Teachers see all assignments
        assignments = crud.get_all_assignments(session=session, skip=skip, limit=limit)
    else:
        # Students see only their own assignments
        assignments = crud.get_student_assignments(
            session=session, student_id=current_user.id, skip=skip, limit=limit
        )
    
    return AssignmentsPublic(data=assignments, count=len(assignments))


@router.get("/all", response_model=AssignmentsPublic)
def get_all_assignments(
    *,
    session: SessionDep,
    current_user: TeacherUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get all assignments (teachers only).
    """
    assignments = crud.get_all_assignments(session=session, skip=skip, limit=limit)
    return AssignmentsPublic(data=assignments, count=len(assignments))


@router.put("/{assignment_id}/grade", response_model=AssignmentPublic)
def grade_assignment(
    *,
    session: SessionDep,
    current_user: TeacherUser,
    assignment_id: uuid.UUID,
    grade: float = Form(..., ge=0, le=100),
    comments: str | None = Form(None),
) -> Any:
    """
    Grade an assignment (teachers only).
    """
    assignment = crud.get_assignment(session=session, assignment_id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Update assignment with grade
    assignment_in = AssignmentUpdate(
        grade=grade,
        comments=comments,
        status="graded",
    )
    
    # Set teacher_id if not already set
    if not assignment.teacher_id:
        assignment.teacher_id = current_user.id
    
    assignment = crud.update_assignment(
        session=session, db_assignment=assignment, assignment_in=assignment_in
    )
    
    return assignment


@router.get("/{assignment_id}/download")
def download_assignment(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    assignment_id: uuid.UUID,
) -> Any:
    """
    Download an assignment file.
    Students can only download their own files, teachers can download any file.
    """
    assignment = crud.get_assignment(session=session, assignment_id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Check permissions
    if current_user.role == "student" and assignment.student_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to download this file",
        )
    
    # Check if file exists
    file_path = Path(assignment.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=assignment.file_name,
        media_type="application/octet-stream",
    )


@router.get("/stats", response_model=AssignmentStats)
def get_assignment_stats(
    *,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Get assignment statistics.
    Students see their own stats, teachers see overall stats.
    """
    if current_user.role == "teacher" or current_user.is_superuser:
        # Teachers see all stats
        stats = crud.get_assignment_stats(session=session)
    else:
        # Students see only their own stats
        stats = crud.get_assignment_stats(session=session, student_id=current_user.id)
    
    return AssignmentStats(**stats)


@router.delete("/{assignment_id}", response_model=Message)
def delete_assignment(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    assignment_id: uuid.UUID,
) -> Any:
    """
    Delete an assignment.
    Students can delete their own assignments, teachers can delete any assignment.
    """
    assignment = crud.get_assignment(session=session, assignment_id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Check permissions
    if current_user.role == "student" and assignment.student_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete this assignment",
        )
    
    # Delete file from disk
    file_path = Path(assignment.file_path)
    if file_path.exists():
        file_path.unlink()
    
    # Delete from database
    session.delete(assignment)
    session.commit()
    
    return Message(message="Assignment deleted successfully")
