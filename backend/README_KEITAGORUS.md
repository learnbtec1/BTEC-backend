# Keitagorus (قيتاغورس AI) - Setup and Usage Guide

## Overview

Keitagorus (قيتاغورس AI) is the AI-powered learning assistant foundation for the BTEC Smart Platform. This document provides instructions for running migrations, seeding demo data, starting the server, and testing the new features.

## Features

- **Authentication**: User registration and login with JWT tokens
- **File Management**: Upload, download, list, and delete files with ownership controls
- **Student Progress Tracking**: Monitor student progress, scores, and struggling indicators
- **AI Assistant**: Query the Keitagorus assistant for personalized recommendations (mock implementation)

## Prerequisites

- Python 3.10+
- PostgreSQL database
- uv package manager (or pip)
- Docker (for running PostgreSQL via docker-compose)

## Setup Instructions

### 1. Database Setup

Start the PostgreSQL database using docker-compose:

```bash
cd /path/to/BTEC-backend
docker compose up -d db
```

### 2. Run Migrations

Apply the database migrations to create the necessary tables:

```bash
cd backend
uv run alembic upgrade head
```

Or using the prestart script:

```bash
cd backend
uv run bash scripts/prestart.sh
```

### 3. Seed Demo Data

Create demo users, lessons, and sample data:

```bash
cd backend
uv run python scripts/seed_demo.py
```

This will create:
- 3 demo users (student, teacher, admin)
- 4 sample lessons
- Student progress records
- Sample file uploads

### Demo Credentials

After running the seed script, you can use these credentials:

- **Student**: `student1@example.com` / `student123`
- **Teacher**: `teacher1@example.com` / `teacher123`
- **Admin**: `admin@example.com` / `admin123`

### 4. Start the Server

Run the FastAPI development server:

```bash
cd backend
uv run fastapi dev app/main.py
```

The API will be available at: `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`

## API Endpoints

### Authentication

#### Register a New User

**POST** `/api/v1/login/register`

```bash
curl -X POST "http://localhost:8000/api/v1/login/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "password123",
    "full_name": "New User"
  }'
```

#### Login (Get Access Token)

**POST** `/api/v1/login/access-token`

```bash
curl -X POST "http://localhost:8000/api/v1/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student1@example.com&password=student123"
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### Test Token

**POST** `/api/v1/login/test-token`

```bash
curl -X POST "http://localhost:8000/api/v1/login/test-token" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### File Management

#### Upload a File

**POST** `/api/v1/files/upload`

```bash
curl -X POST "http://localhost:8000/api/v1/files/upload" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@/path/to/your/file.pdf"
```

#### List User Files

**GET** `/api/v1/files`

```bash
curl -X GET "http://localhost:8000/api/v1/files" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Download a File

**GET** `/api/v1/files/{file_id}`

```bash
curl -X GET "http://localhost:8000/api/v1/files/{FILE_ID}" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -o downloaded_file.pdf
```

#### Delete a File

**DELETE** `/api/v1/files/{file_id}`

```bash
curl -X DELETE "http://localhost:8000/api/v1/files/{FILE_ID}" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### AI Assistant

#### Query the Assistant

**POST** `/api/v1/assistant/query`

```bash
curl -X POST "http://localhost:8000/api/v1/assistant/query" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Help me with my progress",
    "context": null
  }'
```

Response:
```json
{
  "answer": "You've completed 3 lessons with an average score of 70.2%.",
  "recommendations": [
    "Review the lesson materials for better understanding",
    "Consider reviewing the lessons where you're struggling"
  ],
  "actions": [
    "view_progress_dashboard",
    "view_detailed_analytics"
  ]
}
```

## Testing

### Run All Tests

```bash
cd backend
uv run bash scripts/tests-start.sh
```

### Run Specific Tests

```bash
cd backend
uv run pytest tests/test_files_and_assistant.py -v
```

## Security Notes

⚠️ **Important Security Considerations**:

1. **Register Endpoint**: The `/api/v1/login/register` endpoint is for **development only**. In production, implement proper email verification and rate limiting.

2. **Secret Key**: Change the `SECRET_KEY` in your `.env` file to a secure random value:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **File Uploads**: The current implementation has basic file validation. Add additional security measures:
   - File type validation
   - File size limits
   - Virus scanning
   - Content sanitization

4. **CORS**: The CORS settings include `localhost:3001` for development. Update for production environments.

## Environment Variables

Key environment variables (see `.env.example`):

```env
# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=11520

# Database
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changethis
POSTGRES_DB=app

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
FRONTEND_HOST=http://localhost:5173
```

## Troubleshooting

### Database Connection Issues

If you encounter database connection errors:

1. Ensure PostgreSQL is running: `docker compose ps`
2. Check database credentials in `.env`
3. Verify database exists: `docker compose exec db psql -U postgres -l`

### Migration Issues

If migrations fail:

1. Check current migration status: `cd backend && uv run alembic current`
2. Review migration history: `uv run alembic history`
3. Rollback if needed: `uv run alembic downgrade -1`

### File Upload Issues

If file uploads fail:

1. Ensure `uploads/` directory is writable
2. Check disk space
3. Verify file size is within limits

## Next Steps

Future enhancements for Keitagorus:

1. **Real AI Integration**: Replace mock assistant with actual AI models (OpenAI, local LLMs, etc.)
2. **WebSocket Streaming**: Implement streaming responses for better UX
3. **Advanced Progress Analytics**: Add detailed charts and insights
4. **Recommendation Engine**: Build sophisticated learning path recommendations
5. **Multi-language Support**: Add Arabic language support throughout
6. **Email Notifications**: Send progress updates and recommendations via email

## Support

For issues or questions, please create an issue in the GitHub repository.
