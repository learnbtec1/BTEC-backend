#!/usr/bin/env bash
set -euo pipefail

# Script to create BTEC backend scaffold files, create branch, and commit.
# It will NOT overwrite existing files (it will skip files that already exist).
# Usage:
#   chmod +x create_btec_files.sh
#   ./create_btec_files.sh

BASE_BRANCH="main"
BRANCH_NAME="feature/infra/fastapi-setup-$(date +%Y%m%d%H%M%S)"

echo "Running in: $(pwd)"
if [ ! -d .git ]; then
  echo "ERROR: this script must be run from the root of a git repository (where .git exists)."
  exit 1
fi

# Create and switch to branch
git fetch origin ${BASE_BRANCH} || true
git checkout -b "${BRANCH_NAME}"

# Helper to write file only if it doesn't exist
write_if_missing() {
  local path="$1"
  local content="$2"
  if [ -e "$path" ]; then
    echo "SKIP (exists): $path"
  else
    mkdir -p "$(dirname "$path")"
    printf "%s" "$content" > "$path"
    echo "CREATED: $path"
  fi
}

# Files and contents
write_if_missing "requirements.txt" "fastapi==0.95.2
uvicorn[standard]==0.22.0
SQLAlchemy==2.0.19
psycopg2-binary==2.9.6
alembic==1.11.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pydantic==1.10.11
pytest==7.4.0
httpx==0.24.1
pytest-asyncio==0.21.0
python-multipart==0.0.6
ruff==0.10.0
black==23.9.1
isort==5.12.0
"

write_if_missing ".env.example" "# Rename to .env for local development
# Local SQLite quick example:
DATABASE_URL=sqlite:///./dev.db

# Production/Postgres example (Render):
# DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>:<port>/<db_name>

SECRET_KEY=replace-with-a-very-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS origins (comma separated) e.g.
# BACKEND_CORS_ORIGINS=http://localhost:10000,http://localhost:5173

# Render placeholders:
RENDER_API_KEY=
RENDER_SERVICE_ID=
POSTGRES_USER=
POSTGRES_PASSWORD=
"

write_if_missing ".secrets_placeholders.md" "# Secrets / placeholders to set in GitHub (Settings > Secrets) and Render env vars

- DATABASE_URL: postgresql+psycopg2://<user>:<password>@<host>:<port>/<dbname>
- SECRET_KEY: secure-long-random-string
- ALGORITHM: HS256
- ACCESS_TOKEN_EXPIRE_MINUTES: 60
- BACKEND_CORS_ORIGINS: comma-separated origins (e.g. http://localhost:10000,http://localhost:5173)
- RENDER_API_KEY: (optional) render.com API key for automated workflows
- RENDER_SERVICE_ID: (optional) render service id for triggering deploys
- POSTGRES_USER / POSTGRES_PASSWORD: optional, if you provision DB on Render
"

write_if_missing "render.yaml" "service:
  name: btec-backend
  env: python
  plan: starter
  buildCommand: \"pip install -r requirements.txt\"
  startCommand: \"uvicorn main:app --host 0.0.0.0 --port 10000\"
  releaseCommand: \"alembic -c alembic.ini upgrade head\"
  envVars:
    - key: DATABASE_URL
      value: \"{{ DATABASE_URL }}\"
    - key: SECRET_KEY
      value: \"{{ SECRET_KEY }}\"
    - key: ALGORITHM
      value: \"HS256\"
    - key: ACCESS_TOKEN_EXPIRE_MINUTES
      value: \"60\"

databases:
  - name: btec-backend-db
    engine: postgres
    plan: starter
"

write_if_missing "Dockerfile" "# Dockerfile for production
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y build-essential libpq-dev gcc \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 10000

CMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"10000\"]
"

write_if_missing "main.py" "# Top-level entry so render startCommand can use \"uvicorn main:app\"
from app.main import app
"

# app package files (skip app/main.py if exists)
write_if_missing "app/__init__.py" "# package marker
"

write_if_missing "app/core/config.py" "from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = \"sqlite:///./dev.db\"
    SECRET_KEY: str = \"please-change-this-secret\"
    ALGORITHM: str = \"HS256\"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    BACKEND_CORS_ORIGINS: Optional[str] = None
    CREATE_DB_ON_STARTUP: bool = True

    class Config:
        env_file = \".env\"
        env_file_encoding = \"utf-8\"

settings = Settings()
"

write_if_missing "app/core/security.py" "from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from app.core.config import settings

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = {\"sub\": str(subject)}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({\"exp\": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise
"

write_if_missing "app/db/session.py" "from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# Using synchronous engine for compatibility (simple and works with psycopg2 and sqlite)
engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"

write_if_missing "app/models/user.py" "from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.session import Base

class User(Base):
    __tablename__ = \"users\"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    hashed_password = Column(String(512), nullable=False)
    is_active = Column(Boolean(), default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
"

write_if_missing "app/schemas/user.py" "from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[str] = None
"

write_if_missing "app/crud/user.py" "from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=[\"bcrypt\"], deprecated=\"auto\")

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str) -> User:
    hashed_password = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
"

write_if_missing "app/api/deps.py" "from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from app.crud.user import get_user_by_email
from jose import JWTError

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        email = payload.get(\"sub\")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Invalid token")
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"User not found")
    return user
"

write_if_missing "app/api/routes/auth.py" "from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead, Token
from app.db.session import get_db
from app.crud.user import get_user_by_email, create_user, verify_password
from app.core.security import create_access_token

router = APIRouter()

@router.post(\"/register\", response_model=UserRead)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=\"Email already registered\")
    user = create_user(db, payload.email, payload.password)
    return user

@router.post(\"/login\", response_model=Token)
def login(payload: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Incorrect credentials\")
    access_token = create_access_token(subject=user.email)
    return {\"access_token\": access_token, \"token_type\": \"bearer\"}
"

write_if_missing "app/api/routes/health.py" "from fastapi import APIRouter
from app.db.session import engine
from sqlalchemy import text

router = APIRouter()

@router.get(\"/health\")
def health():
    db_ok = False
    try:
        # simple SELECT 1 to ensure DB connectivity
        with engine.connect() as conn:
            conn.execute(text(\"SELECT 1\"))
            db_ok = True
    except Exception:
        db_ok = False
    return {\"status\": \"ok\", \"db\": db_ok}
"

# Alembic files
write_if_missing "alembic.ini" "[alembic]
script_location = alembic
sqlalchemy.url = %(DATABASE_URL)s

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
"

write_if_missing "alembic/env.py" "import os
from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context

config = context.config
fileConfig(config.config_file_name)

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.db.session import Base
target_metadata = Base.metadata

def get_url():
    return os.environ.get(\"DATABASE_URL\", config.get_main_option(\"sqlalchemy.url\"))

def run_migrations_offline():
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(get_url(), future=True)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"

write_if_missing "alembic/script.py.mako" "%# Alembic migration script template
"

write_if_missing "alembic/versions/0001_initial.py" "\"\"\"initial migration

Revision ID: 0001
Revises: 
Create Date: 2025-12-30 00:00:00.000000
\"\"\"
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(length=256), nullable=False),
        sa.Column('hashed_password', sa.String(length=512), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
"

write_if_missing "tests/test_auth.py" "import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import Base, engine

client = TestClient(app)

@pytest.fixture(scope=\"module\", autouse=True)
def setup_db():
    # Create tables for tests (uses configured DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_health():
    r = client.get(\"/api/health\")
    assert r.status_code == 200
    data = r.json()
    assert \"status\" in data
    assert data[\"status\"] == \"ok\"

def test_register_and_login():
    email = \"test@example.com\"
    password = \"strongpassword\"
    # register
    response = client.post(\"/api/auth/register\", json={\"email\": email, \"password\": password})
    assert response.status_code == 200
    data = response.json()
    assert data[\"email\"] == email

    # login
    response = client.post(\"/api/auth/login\", json={\"email\": email, \"password\": password})
    assert response.status_code == 200
    token_data = response.json()
    assert \"access_token\" in token_data
    assert token_data[\"token_type\"] == \"bearer\"
"

# Workflows
write_if_missing ".github/workflows/test.yml" "name: Test

on:
  push:
    branches:
      - \"**\"
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest -q
"

write_if_missing ".github/workflows/lint.yml" "name: Lint

on:
  push:
    branches:
      - \"**\"
  pull_request:
    branches:
      - main

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install linters
        run: |
          python -m pip install --upgrade pip
          pip install ruff black isort
      - name: Run ruff
        run: ruff check .
      - name: Run black check
        run: black --check .
      - name: Run isort check
        run: isort --check-only .
"

write_if_missing ".github/workflows/deploy-render.yml" "name: Deploy to Render (template)

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install requirements
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      # NOTE: The workflow below uses Render's API to trigger deploy.
      # It requires RENDER_API_KEY and RENDER_SERVICE_ID secrets to be set.
      - name: Trigger Render deploy
        if: ${{ secrets.RENDER_API_KEY && secrets.RENDER_SERVICE_ID }}
        run: |
          curl -X POST \"https://api.render.com/deploy/srv-${{ secrets.RENDER_SERVICE_ID }}/deploys\" \
            -H \"Accept: application/json\" \
            -H \"Authorization: Bearer ${{ secrets.RENDER_API_KEY }}\" \
            -H \"Content-Type: application/json\" \
            -d '{}'
"

write_if_missing "architecture.md" "# Architecture — BTEC Backend

Components:
- FastAPI application (this repo)
- PostgreSQL database (Render managed DB)
- Frontend:
  - Flutter mobile app (Android)
  - React web app (Vercel)
- CI: GitHub Actions (lint, test, build, deploy trigger)
- Deployment: Render (web service + managed Postgres)

Flow:
- Developer pushes feature branch → opens PR → CI runs linters and tests
- On merge to main, Render deploy (via UI or API) will build and start service
- releaseCommand runs alembic to migrate DB schema
- JWT tokens used for stateless auth between frontends and backend
"

write_if_missing "sprint-plan.md" "# Sprint Plan — Initial Setup (BTEC Backend)

Sprint: Infra & Auth (2 weeks)

Epics / Tasks:
- [ ] Project scaffold (FastAPI, app structure)
- [ ] Database integration (SQLAlchemy, Alembic)
- [ ] Auth endpoints (register/login with JWT)
- [ ] Health check + CORS configuration
- [ ] Tests (pytest)
- [ ] CI workflows (lint, test)
- [ ] Render configuration (render.yaml, Dockerfile)
- [ ] Documentation (README, architecture)
- [ ] Create GitHub issues for further features (user profile, roles, endpoints)
"

write_if_missing "issues/initial_issues.yaml" "# Initial issues to create manually or via script
- title: \"Implement user profile endpoints\"
  body: \"Add endpoints to read/update user profile (GET /api/users/me, PUT /api/users/me).\"
  labels: [\"feature\", \"backend\"]

- title: \"Add role-based access control\"
  body: \"Add roles (admin, user) and protect routes accordingly.\"
  labels: [\"feature\", \"security\"]

- title: \"Add pagination helpers\"
  body: \"Implement common pagination utilities and apply to list endpoints.\"
  labels: [\"chore\"]
"

write_if_missing ".github/ISSUE_TEMPLATE/bug_report.md" "--- 
name: Bug report
about: Create a report to help us improve
title: '[Bug] '
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. ...
2. ...
3. ...

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots / Logs**
If applicable, add screenshots or logs to help explain your problem.

**Additional context**
Add any other context about the problem here.
"

write_if_missing ".github/ISSUE_TEMPLATE/feature_request.md" "--- 
name: Feature request
about: Suggest an idea for this project
title: '[Feature] '
labels: enhancement
assignees: ''

---

**Is your feature request related to a problem? Please describe.**

**Describe the solution you'd like**

**Additional context**
"

write_if_missing "PR_BODY.md" "Chore: setup FastAPI backend, CI/CD, docs, and Render deploy

What I added:
- FastAPI scaffold in \`app/\` with auth and health endpoints
  - POST /api/auth/register
  - POST /api/auth/login
  - GET /api/health (also checks DB connectivity)
- SQLAlchemy models and DB session
- Alembic initial migration (alembic/versions/0001_initial.py)
- Tests for health and auth (pytest)
- Dockerfile and render.yaml (releaseCommand runs Alembic)
- .env.example and .secrets_placeholders.md
- GitHub workflows: lint, test, deploy-render (template)
- Docs: README.md, architecture.md, sprint-plan.md, issues list
- Issue templates

How to run locally:
1. cp .env.example .env
2. pip install -r requirements.txt
3. alembic -c alembic.ini upgrade head
4. uvicorn main:app --reload --host 0.0.0.0 --port 10000

Secrets required (add to GitHub repo settings and Render env):
- DATABASE_URL
- SECRET_KEY
- ALGORITHM (HS256)
- ACCESS_TOKEN_EXPIRE_MINUTES
- RENDER_API_KEY (optional)
- RENDER_SERVICE_ID (optional)

Notes:
- I did NOT merge this PR automatically. Please review and merge after checks pass.
- After merging, configure Render service (or use render.yaml) and ensure secrets are set before deploying.
"

write_if_missing "README.md" "# BTEC Backend — FastAPI

BTEC Smart Platform — Backend service

Stack:
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL (Render)
- JWT (python-jose)
- Passwords hashed with passlib
- CI: GitHub Actions (lint, test)
- Deployment target: Render (render.yaml included)

Quick overview
--------------
- Health endpoint: GET /api/health (also checks DB connectivity)
- Auth endpoints:
  - POST /api/auth/register
  - POST /api/auth/login

Local quickstart (SQLite)
-------------------------
1. Copy env file:
   cp .env.example .env
2. Create and activate virtualenv:
   python -m venv .venv
   source .venv/bin/activate
3. Install dependencies:
   pip install --upgrade pip
   pip install -r requirements.txt
4. Run migrations:
   alembic -c alembic.ini upgrade head
   (If using SQLite local, migrations should work with the provided script)
5. Run server:
   uvicorn main:app --reload --host 0.0.0.0 --port 10000
6. Visit:
   - Health: GET http://127.0.0.1:10000/api/health
   - Docs: http://127.0.0.1:10000/docs

PostgreSQL / Render
-------------------
- Update DATABASE_URL in Settings or add it as GitHub/Render secret.
- The included \`render.yaml\` specifies:
  - releaseCommand: \`alembic -c alembic.ini upgrade head\`
  - startCommand: \`uvicorn main:app --host 0.0.0.0 --port 10000\`

Secrets to add (GitHub Secrets & Render env vars)
- DATABASE_URL (e.g. postgresql+psycopg2://user:pass@host:5432/dbname)
- SECRET_KEY (use a long random value)
- ALGORITHM (HS256)
- ACCESS_TOKEN_EXPIRE_MINUTES (e.g. 60)
- RENDER_API_KEY (optional, for automated deploys)
- RENDER_SERVICE_ID (optional)

CI
--
- A test workflow is included at \`.github/workflows/test.yml\`.
- A lint workflow is included at \`.github/workflows/lint.yml\`.
- A deploy workflow template is included at \`.github/workflows/deploy-render.yml\` (uses placeholders for secrets).

Notes and recommendations
-------------------------
- Do NOT commit real secret values to the repo.
- For production, set specific \`BACKEND_CORS_ORIGINS\` instead of allowing all origins.
- Consider adding rate-limiting, logging, and monitoring for production.
"

echo "----"
echo "All files created (where missing)."
git add .
git commit -m "chore: setup FastAPI backend, CI/CD, docs, and Render deploy" || echo "No changes to commit (files may already exist)"
echo "Branch ready: ${BRANCH_NAME}"
echo "Now run:"
echo "  git push --set-upstream origin ${BRANCH_NAME}"
echo "Then create PR, e.g.:"
echo "  gh pr create --title \"chore: setup FastAPI backend, CI/CD, docs, and Render deploy\" --body \"$(printf 'See PR_BODY.md')\" --base main"