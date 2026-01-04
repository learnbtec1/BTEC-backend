#!/usr/bin/env python3
"""
Seed demo data for Keitagorus platform.

This script creates:
- Demo users (student, teacher, admin)
- Sample courses/lessons
- Student progress records
- Example uploaded files

Usage:
    python -m backend.scripts.seed_demo
    
Or from backend directory:
    python scripts/seed_demo.py
"""
import os
import sys
import uuid
from pathlib import Path
from datetime import datetime, timezone

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlmodel import Session, select

from app.core.db import engine
from app.core.security import get_password_hash
from app.models import User, Item
from app.models_files import UserFile
from app.models_progress import StudentProgress


def create_demo_users(session: Session) -> dict[str, User]:
    """Create demo user accounts."""
    print("Creating demo users...")
    
    users = {}
    demo_accounts = [
        {
            "email": "student1@example.com",
            "password": "student123",
            "full_name": "Student One",
            "is_superuser": False,
        },
        {
            "email": "teacher1@example.com",
            "password": "teacher123",
            "full_name": "Teacher One",
            "is_superuser": False,
        },
        {
            "email": "admin@example.com",
            "password": "admin123",
            "full_name": "Admin User",
            "is_superuser": True,
        },
    ]
    
    for account in demo_accounts:
        # Check if user already exists
        existing = session.exec(
            select(User).where(User.email == account["email"])
        ).first()
        
        if existing:
            print(f"  ✓ User {account['email']} already exists")
            users[account["email"]] = existing
        else:
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
            print(f"  ✓ Created user: {account['email']}")
    
    return users


def create_sample_items(session: Session, users: dict[str, User]) -> list[Item]:
    """Create sample lesson/course items."""
    print("\nCreating sample lessons...")
    
    items = []
    student = users["student1@example.com"]
    
    sample_lessons = [
        {"title": "Introduction to Python Programming", "description": "Learn the basics of Python"},
        {"title": "Web Development Fundamentals", "description": "HTML, CSS, and JavaScript basics"},
        {"title": "Database Design Principles", "description": "SQL and database modeling"},
        {"title": "BTEC Unit 1: Programming", "description": "Core programming concepts"},
        {"title": "BTEC Unit 2: Networking", "description": "Network fundamentals"},
    ]
    
    for lesson_data in sample_lessons:
        item = Item(
            title=lesson_data["title"],
            description=lesson_data["description"],
            owner_id=student.id,
        )
        session.add(item)
        items.append(item)
    
    session.commit()
    for item in items:
        session.refresh(item)
    
    print(f"  ✓ Created {len(items)} sample lessons")
    return items


def create_progress_records(session: Session, users: dict[str, User], items: list[Item]) -> None:
    """Create student progress records."""
    print("\nCreating progress records...")
    
    student = users["student1@example.com"]
    
    # Create progress for each lesson
    progress_data = [
        {"progress": 100, "score": 85.5, "attempts": 2, "struggling": False},
        {"progress": 75, "score": 72.0, "attempts": 3, "struggling": False},
        {"progress": 50, "score": 65.0, "attempts": 4, "struggling": True},
        {"progress": 25, "score": 55.0, "attempts": 5, "struggling": True},
        {"progress": 10, "score": None, "attempts": 1, "struggling": False},
    ]
    
    for i, item in enumerate(items):
        data = progress_data[i] if i < len(progress_data) else progress_data[0]
        
        progress = StudentProgress(
            user_id=student.id,
            lesson_id=item.id,
            progress_percentage=data["progress"],
            last_score=data["score"],
            attempts=data["attempts"],
            struggling=data["struggling"],
            updated_at=datetime.now(timezone.utc),
        )
        session.add(progress)
    
    session.commit()
    print(f"  ✓ Created {len(items)} progress records")


def create_sample_files(session: Session, users: dict[str, User]) -> None:
    """Create sample file records with dummy files."""
    print("\nCreating sample files...")
    
    student = users["student1@example.com"]
    
    # Create uploads directory
    upload_base = Path("/home/runner/work/BTEC-backend/BTEC-backend/uploads")
    user_dir = upload_base / str(student.id)
    user_dir.mkdir(parents=True, exist_ok=True)
    
    sample_files = [
        {"name": "assignment1.pdf", "content": b"PDF content placeholder", "type": "application/pdf"},
        {"name": "notes.txt", "content": b"My study notes for BTEC Unit 1", "type": "text/plain"},
        {"name": "project.zip", "content": b"ZIP archive placeholder", "type": "application/zip"},
    ]
    
    for file_data in sample_files:
        # Generate unique file ID
        file_id = uuid.uuid4()
        file_ext = Path(file_data["name"]).suffix
        stored_filename = f"{file_id}{file_ext}"
        file_path = user_dir / stored_filename
        
        # Write dummy content
        with open(file_path, "wb") as f:
            f.write(file_data["content"])
        
        # Create database record
        db_file = UserFile(
            id=file_id,
            owner_id=student.id,
            original_filename=file_data["name"],
            stored_path=str(file_path),
            content_type=file_data["type"],
            size=len(file_data["content"]),
            created_at=datetime.now(timezone.utc),
        )
        session.add(db_file)
    
    session.commit()
    print(f"  ✓ Created {len(sample_files)} sample files")


def main() -> None:
    """Main seeding function."""
    print("=" * 60)
    print("Keitagorus Demo Data Seeding")
    print("=" * 60)
    
    with Session(engine) as session:
        # Create users
        users = create_demo_users(session)
        
        # Create sample lessons
        items = create_sample_items(session, users)
        
        # Create progress records
        create_progress_records(session, users, items)
        
        # Create sample files
        create_sample_files(session, users)
    
    print("\n" + "=" * 60)
    print("✓ Demo data seeding completed successfully!")
    print("=" * 60)
    print("\nDemo Credentials:")
    print("  Student: student1@example.com / student123")
    print("  Teacher: teacher1@example.com / teacher123")
    print("  Admin:   admin@example.com / admin123")
    print("=" * 60)


if __name__ == "__main__":
    main()
