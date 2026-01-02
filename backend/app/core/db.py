from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    # Create superuser
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            username="admin",
            role="teacher",
        )
        user = crud.create_user(session=session, user_create=user_in)
    
    # Create teacher1
    teacher = session.exec(
        select(User).where(User.username == "teacher1")
    ).first()
    if not teacher:
        teacher_in = UserCreate(
            email="teacher1@btec.edu",
            password="1234",
            username="teacher1",
            role="teacher",
            full_name="Teacher One",
            is_superuser=False,
        )
        teacher = crud.create_user(session=session, user_create=teacher_in)
    
    # Create 10 students (user1 to user10)
    for i in range(1, 11):
        username = f"user{i}"
        student = session.exec(
            select(User).where(User.username == username)
        ).first()
        if not student:
            student_in = UserCreate(
                email=f"user{i}@btec.edu",
                password="1234",
                username=username,
                role="student",
                full_name=f"Student {i}",
                is_superuser=False,
            )
            student = crud.create_user(session=session, user_create=student_in)
