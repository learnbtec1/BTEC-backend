#!/usr/bin/env python3
"""
Demo seed script for Keitagorus foundation.

This script creates demo users, sample courses/lessons, student progress records,
and sample file uploads for testing purposes.

Usage:
    cd backend
    uv run python scripts/seed_demo.py
"""

import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.core.db import engine
from app.core.security import get_password_hash
from app.models import Item, User
from app.models_files import UserFile
from app.models_progress import StudentProgress


def create_demo_users(session: Session) -> dict[str, User]:
    """Create demo users if they don't exist."""
    users = {}
    
    demo_accounts = [
        {
            "email": "student1@example.com",
            "password": "student123",
            "full_name": "Demo Student 1",
            "is_superuser": False,
        },
        {
            "email": "teacher1@example.com",
            "password": "teacher123",
            "full_name": "Demo Teacher 1",
            "is_superuser": False,
        },
        {
            "email": "admin@example.com",
            "password": "admin123",
            "full_name": "Demo Admin",
            "is_superuser": True,
        },
    ]
    
    for account in demo_accounts:
        # Check if user exists
        statement = select(User).where(User.email == account["email"])
        existing_user = session.exec(statement).first()
        
        if existing_user:
            print(f"✓ User {account['email']} already exists")
            users[account["email"]] = existing_user
        else:
            # Create new user
            user = User(
                email=account["email"],
                hashed_password=get_password_hash(account["password"]),
                full_name=account["full_name"],
                is_superuser=account["is_superuser"],
                is_active=True,
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            users[account["email"]] = user
            print(f"✓ Created user {account['email']}")
    
    return users


def create_sample_lessons(session: Session, users: dict[str, User]) -> list[Item]:
    """Create sample lessons (items)."""
    lessons = []
    teacher = users["teacher1@example.com"]
    
    sample_lessons = [
        {
            "title": "Introduction to Python Programming",
            "description": "Learn the basics of Python programming language",
        },
        {
            "title": "Web Development Fundamentals",
            "description": "HTML, CSS, and JavaScript basics",
        },
        {
            "title": "Database Design Principles",
            "description": "Learn how to design efficient databases",
        },
        {
            "title": "API Development with FastAPI",
            "description": "Build modern APIs with FastAPI framework",
        },
    ]
    
    for lesson_data in sample_lessons:
        # Check if lesson exists
        statement = select(Item).where(
            Item.title == lesson_data["title"],
            Item.owner_id == teacher.id
        )
        existing_lesson = session.exec(statement).first()
        
        if existing_lesson:
            lessons.append(existing_lesson)
        else:
            lesson = Item(
                title=lesson_data["title"],
                description=lesson_data["description"],
                owner_id=teacher.id,
            )
            session.add(lesson)
            session.commit()
            session.refresh(lesson)
            lessons.append(lesson)
            print(f"✓ Created lesson: {lesson.title}")
    
    return lessons


def create_student_progress(
    session: Session, 
    users: dict[str, User], 
    lessons: list[Item]
) -> None:
    """Create sample student progress records."""
    student = users["student1@example.com"]
    
    # Create progress for some lessons
    progress_data = [
        {
            "lesson_id": lessons[0].id,
            "progress_percentage": 100,
            "last_score": 85.5,
            "attempts": 2,
            "struggling": False,
        },
        {
            "lesson_id": lessons[1].id,
            "progress_percentage": 60,
            "last_score": 55.0,
            "attempts": 3,
            "struggling": True,
        },
        {
            "lesson_id": lessons[2].id,
            "progress_percentage": 30,
            "last_score": 70.0,
            "attempts": 1,
            "struggling": False,
        },
    ]
    
    for data in progress_data:
        # Check if progress exists
        statement = select(StudentProgress).where(
            StudentProgress.user_id == student.id,
            StudentProgress.lesson_id == data["lesson_id"]
        )
        existing_progress = session.exec(statement).first()
        
        if not existing_progress:
            progress = StudentProgress(
                user_id=student.id,
                lesson_id=data["lesson_id"],
                progress_percentage=data["progress_percentage"],
                last_score=data["last_score"],
                attempts=data["attempts"],
                struggling=data["struggling"],
                updated_at=datetime.now(timezone.utc),
            )
            session.add(progress)
            print(f"✓ Created progress record for lesson {data['lesson_id']}")
    
    session.commit()


def create_sample_files(session: Session, users: dict[str, User]) -> None:
    """Create sample file records with dummy files."""
    student = users["student1@example.com"]
    
    # Create uploads directory structure
    upload_dir = Path("uploads") / str(student.id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Create dummy files
    sample_files = [
        {
            "original_filename": "assignment1.pdf",
            "content": b"This is a sample PDF file content",
            "content_type": "application/pdf",
        },
        {
            "original_filename": "notes.txt",
            "content": b"Sample notes for the course",
            "content_type": "text/plain",
        },
    ]
    
    for file_data in sample_files:
        # Create dummy file on disk
        file_uuid = uuid.uuid4()
        file_extension = Path(file_data["original_filename"]).suffix
        stored_filename = f"{file_uuid}{file_extension}"
        file_path = upload_dir / stored_filename
        
        # Check if file record exists
        statement = select(UserFile).where(
            UserFile.owner_id == student.id,
            UserFile.original_filename == file_data["original_filename"]
        )
        existing_file = session.exec(statement).first()
        
        if not existing_file:
            # Write dummy content to file
            with open(file_path, "wb") as f:
                f.write(file_data["content"])
            
            # Create database record
            user_file = UserFile(
                owner_id=student.id,
                original_filename=file_data["original_filename"],
                stored_path=str(file_path),
                content_type=file_data["content_type"],
                size=len(file_data["content"]),
                created_at=datetime.now(timezone.utc),
            )
            session.add(user_file)
            print(f"✓ Created file: {file_data['original_filename']}")
    
    session.commit()


def main():
    """Main function to seed demo data."""
    print("\n=== Keitagorus Demo Seed Script ===\n")
    
    with Session(engine) as session:
        try:
            # Create demo users
            print("Creating demo users...")
            users = create_demo_users(session)
            
            # Create sample lessons
            print("\nCreating sample lessons...")
            lessons = create_sample_lessons(session, users)
            
            # Create student progress
            print("\nCreating student progress records...")
            create_student_progress(session, users, lessons)
            
            # Create sample files
            print("\nCreating sample files...")
            create_sample_files(session, users)
            
            print("\n=== Demo data seeded successfully! ===\n")
            print("Demo credentials:")
            print("  Student: student1@example.com / student123")
            print("  Teacher: teacher1@example.com / teacher123")
            print("  Admin:   admin@example.com / admin123")
            print()
            
        except Exception as e:
            print(f"\n❌ Error seeding demo data: {e}")
            session.rollback()
            raise


if __name__ == "__main__":
    main()
