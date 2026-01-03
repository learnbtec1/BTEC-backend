"""
Example usage of Phase 3 features: AR Support and Virtual Tutor

This script demonstrates how to use the new StudentProgress tracking
and virtual tutor recommendation features.
"""

from uuid import UUID

from sqlmodel import Session

from app import crud
from app.models import (
    ItemCreate,
    StudentProgressCreate,
    StudentProgressUpdate,
    User,
)
from app.virtual_tutor import recommend_remediation


def example_create_ar_item(session: Session, user_id: UUID) -> None:
    """Example: Create an item with AR model URL."""
    item_data = ItemCreate(
        title="3D Cell Structure",
        description="Interactive 3D model of a cell with organelles",
        ar_model_url="https://cdn.example.com/models/cell-structure.glb",
    )

    item = crud.create_item(session=session, item_in=item_data, owner_id=user_id)
    print(f"Created item with AR model: {item.title}")
    print(f"AR Model URL: {item.ar_model_url}")


def example_track_student_progress(session: Session, user: User) -> None:
    """Example: Track student progress across multiple modules."""
    # Student completes first module with good progress
    progress1 = StudentProgressCreate(
        module_name="Introduction to Biology",
        progress_percentage=85,
        struggling=False,
        last_activity="Completed final quiz with 85%",
    )

    crud.create_or_update_student_progress(
        session=session, user_id=user.id, progress_in=progress1
    )
    print(
        f"Recorded progress for {progress1.module_name}: {progress1.progress_percentage}%"
    )

    # Student starts second module but struggles
    progress2 = StudentProgressCreate(
        module_name="Cell Biology",
        progress_percentage=35,
        struggling=True,
        last_activity="Attempted quiz, scored 35%",
    )

    crud.create_or_update_student_progress(
        session=session, user_id=user.id, progress_in=progress2
    )
    print(
        f"Recorded progress for {progress2.module_name}: {progress2.progress_percentage}%"
    )


def example_update_progress(session: Session, user: User) -> None:
    """Example: Update progress for an existing module."""
    # Student practices and improves
    module_name = "Cell Biology"

    # Get existing progress
    existing = crud.get_student_progress_by_module(
        session=session, user_id=user.id, module_name=module_name
    )

    if existing:
        # Update with improved score
        update = StudentProgressUpdate(
            progress_percentage=65,
            struggling=False,
            last_activity="Retook quiz after studying, scored 65%",
        )

        updated = crud.set_student_progress_fields(
            session=session, progress_obj=existing, progress_update=update
        )

        print(f"\nUpdated {module_name}:")
        print("  Old progress: 35%")
        print(f"  New progress: {updated.progress_percentage}%")
        print(f"  Still struggling: {updated.struggling}")


def example_get_recommendations(session: Session, user: User) -> None:
    """Example: Get personalized tutor recommendations."""
    # Get recommendations with default threshold (60%)
    recommendations = recommend_remediation(session=session, user=user, threshold=60)

    print("\n=== Virtual Tutor Recommendations ===")
    if not recommendations:
        print("Great job! You're doing well in all modules.")
    else:
        for rec in recommendations:
            print(f"\nModule: {rec['module_name']}")
            print(f"Current Progress: {rec['current_progress']}%")
            print(f"Struggling: {rec['struggling']}")
            print("Recommendations:")
            for i, suggestion in enumerate(rec["recommendations"], 1):
                print(f"  {i}. {suggestion}")


def example_query_struggling_modules(session: Session, user: User) -> None:
    """Example: Find modules where student needs help."""
    struggling = crud.get_struggling_modules_for_user(
        session=session, user_id=user.id, progress_threshold=60
    )

    print("\n=== Modules Needing Attention ===")
    if not struggling:
        print("No modules need immediate attention.")
    else:
        for progress in struggling:
            print(f"\n{progress.module_name}:")
            print(f"  Progress: {progress.progress_percentage}%")
            print(f"  Struggling flag: {progress.struggling}")
            print(f"  Last activity: {progress.last_activity or 'None'}")


def example_full_workflow(session: Session, user: User) -> None:
    """Example: Complete workflow from tracking to recommendations."""
    print("=" * 60)
    print("Phase 3 Features Demo: Virtual Tutor System")
    print("=" * 60)

    # 1. Create an item with AR support
    print("\n1. Creating item with AR model...")
    example_create_ar_item(session, user.id)

    # 2. Track student progress
    print("\n2. Tracking student progress...")
    example_track_student_progress(session, user)

    # 3. Update progress after student improves
    print("\n3. Updating progress after practice...")
    example_update_progress(session, user)

    # 4. Get personalized recommendations
    example_get_recommendations(session, user)

    # 5. Query struggling modules
    example_query_struggling_modules(session, user)

    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    # This example assumes you have a database session and user
    # In practice, you would get these from your application context
    print(__doc__)
    print("\nNote: This is a demonstration script.")
    print("To use these features in your application, import and call")
    print("the relevant functions from app.crud and app.virtual_tutor")
