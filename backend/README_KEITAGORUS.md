# Keitagorus (قيتاغورس AI) - Setup Guide

This document provides instructions for setting up and running the Keitagorus AI foundation for the BTEC backend.

## Overview

Keitagorus is an AI-powered learning assistant integrated into the BTEC platform. This foundation includes:

- **Authentication System**: Login and registration endpoints
- **File Management**: Upload, download, and manage user files
- **Progress Tracking**: Monitor student learning progress
- **AI Assistant**: Query-based assistant for personalized learning recommendations

## Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- uv package manager (recommended) or pip

## Environment Setup

1. **Configure Environment Variables**

   Create a `.env` file in the project root (one level above `backend/`):

   ```bash
   # Database
   POSTGRES_SERVER=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=btec_user
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_DB=btec_db
   
   # Security (CHANGE THESE!)
   SECRET_KEY=your-super-secret-key-here
   
   # Project
   PROJECT_NAME="BTEC Smart Platform"
   FIRST_SUPERUSER=admin@example.com
   FIRST_SUPERUSER_PASSWORD=admin_password
   
   # CORS (optional)
   BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:5173
   ```

2. **Install Dependencies**

   From the `backend/` directory:

   ```bash
   cd backend
   uv sync
   ```

   Or with pip:

   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

1. **Run Migrations**

   Apply all database migrations:

   ```bash
   cd backend
   alembic upgrade head
   ```

   This will create the following tables:
   - `user` - User accounts
   - `item` - Lessons/courses
   - `userfile` - File upload metadata
   - `studentprogress` - Learning progress tracking

2. **Seed Demo Data**

   Populate the database with demo accounts and sample data:

   ```bash
   cd backend
   python scripts/seed_demo.py
   ```

   This creates:
   - 3 demo user accounts (student, teacher, admin)
   - 5 sample lessons
   - Progress records with various completion states
   - 3 example uploaded files

## Running the Server

Start the FastAPI development server:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Demo Credentials

After seeding, you can log in with:

| Role    | Email                    | Password    |
|---------|--------------------------|-------------|
| Student | student1@example.com     | student123  |
| Teacher | teacher1@example.com     | teacher123  |
| Admin   | admin@example.com        | admin123    |

## Testing the API

### 1. Get Access Token

```bash
curl -X POST "http://localhost:8000/api/v1/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student1@example.com&password=student123"
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### 2. Upload a File

```bash
curl -X POST "http://localhost:8000/api/v1/files/upload" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@/path/to/your/file.pdf"
```

### 3. List Your Files

```bash
curl -X GET "http://localhost:8000/api/v1/files/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 4. Query the AI Assistant

```bash
curl -X POST "http://localhost:8000/api/v1/assistant/query" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Help me with my progress",
    "context": "I am struggling with programming"
  }'
```

Response:
```json
{
  "answer": "You have 5 lesson(s) in progress...",
  "recommendations": [
    "Focus on fundamentals before moving forward",
    "Try breaking down complex topics into smaller parts"
  ],
  "actions": ["view_detailed_progress"]
}
```

### 5. Download a File

```bash
curl -X GET "http://localhost:8000/api/v1/files/{file_id}" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  --output downloaded_file.pdf
```

### 6. Delete a File

```bash
curl -X DELETE "http://localhost:8000/api/v1/files/{file_id}" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Running Tests

Run the integration tests:

```bash
cd backend
pytest tests/test_files_and_assistant.py -v
```

Run all tests:

```bash
pytest -v
```

With coverage:

```bash
pytest --cov=app tests/
```

## Security Notes

⚠️ **IMPORTANT SECURITY WARNINGS**:

1. **Registration Endpoint**: The `/api/v1/login/register` endpoint is for **development only**. In production:
   - Disable this endpoint or add proper rate limiting
   - Implement email verification
   - Add CAPTCHA protection
   - Add proper input validation and sanitization

2. **Secret Keys**: Never commit real secrets to version control. Always use strong, randomly generated secrets in production:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **File Uploads**: Current implementation stores files on local disk. For production:
   - Consider using cloud storage (S3, Azure Blob, etc.)
   - Add virus scanning
   - Implement file size limits
   - Add file type validation
   - Set up proper backup strategies

4. **CORS**: Configure CORS origins appropriately for your deployment environment.

## File Structure

```
backend/
├── app/
│   ├── api/
│   │   └── api_v1/
│   │       └── endpoints/
│   │           ├── login.py          # Auth endpoints
│   │           ├── files.py          # File management
│   │           └── assistant.py      # AI assistant
│   ├── models.py                     # Core models
│   ├── models_files.py               # File models
│   ├── models_progress.py            # Progress tracking models
│   └── alembic/
│       └── versions/
│           └── a1b2c3d4e5f6_*.py    # Keitagorus migration
├── scripts/
│   └── seed_demo.py                  # Demo data seeding
└── tests/
    └── test_files_and_assistant.py   # Integration tests
```

## Troubleshooting

### Migration Issues

If you encounter migration errors:

```bash
# Check current migration status
alembic current

# View migration history
alembic history

# Downgrade if needed
alembic downgrade -1

# Upgrade to head
alembic upgrade head
```

### Database Connection Issues

Verify your database is running and credentials are correct:

```bash
psql -h localhost -U btec_user -d btec_db
```

### Import Errors

Make sure you're running commands from the correct directory and have activated your virtual environment.

## Future Enhancements

The following features are planned for future iterations:

- [ ] WebSocket streaming for real-time AI responses
- [ ] Integration with actual LLM models (OpenAI, Anthropic, etc.)
- [ ] Advanced file processing (OCR, document parsing)
- [ ] Multi-language support for AI responses
- [ ] Enhanced progress analytics and visualization
- [ ] Collaborative learning features
- [ ] Integration with AR/VR content (ar_model_url field)

## Support

For issues or questions:
- Check the API documentation at `/docs`
- Review test files for usage examples
- Consult the main project README

## License

See the main project LICENSE file for details.
