# Assignment Management System - Setup Guide

## Overview

This system provides a complete file upload and grading platform for teachers and students, featuring:

- **Role-based access control** (Teachers and Students)
- **File upload system** with validation
- **Grading functionality** for teachers
- **Statistics and dashboards** for both roles
- **RESTful API** with JWT authentication

## Quick Start

### 1. Setup Database

Make sure PostgreSQL is running and update the `.env` file with your database credentials:

```bash
# In the root directory
cp .env.example .env
# Edit .env with your settings
```

### 2. Install Dependencies

```bash
cd backend
pip install -e .
# or
pip install fastapi sqlmodel pydantic pydantic-settings alembic psycopg passlib bcrypt pyjwt email-validator python-multipart
```

### 3. Run Migrations

```bash
cd backend
export PYTHONPATH=$(pwd):$PYTHONPATH
alembic upgrade head
```

This will:
- Create the User and Assignment tables
- Add username and role fields to users
- Set up foreign key relationships

### 4. Initialize Data

```bash
cd backend
python -m app.initial_data
```

This creates:
- **1 Teacher**: `teacher1` (email: `teacher1@btec.edu`, password: `1234`)
- **10 Students**: `user1` to `user10` (emails: `user1@btec.edu` to `user10@btec.edu`, password: `1234`)

### 5. Start the Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Testing the API

### Run Component Tests

```bash
python test_assignment_api.py
```

This validates:
- Model imports
- CRUD functions
- File validation
- API endpoint structure

### Manual Testing with curl

See `ASSIGNMENT_API_DOCS.md` for detailed API examples.

#### Quick Test Flow:

```bash
# 1. Login as student
curl -X POST "http://localhost:8000/api/v1/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user1@btec.edu&password=1234"

# Save the token
export STUDENT_TOKEN="<your_token>"

# 2. Upload an assignment
curl -X POST "http://localhost:8000/api/v1/assignments/upload" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -F "title=Math Homework" \
  -F "description=Chapter 1 exercises" \
  -F "file=@test_file.pdf"

# 3. View your assignments
curl -X GET "http://localhost:8000/api/v1/assignments/my" \
  -H "Authorization: Bearer $STUDENT_TOKEN"

# 4. Login as teacher
curl -X POST "http://localhost:8000/api/v1/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teacher1@btec.edu&password=1234"

export TEACHER_TOKEN="<your_token>"

# 5. View all assignments (teacher)
curl -X GET "http://localhost:8000/api/v1/assignments/all" \
  -H "Authorization: Bearer $TEACHER_TOKEN"

# 6. Grade an assignment (teacher)
curl -X PUT "http://localhost:8000/api/v1/assignments/<assignment_id>/grade" \
  -H "Authorization: Bearer $TEACHER_TOKEN" \
  -F "grade=95" \
  -F "comments=Excellent work!"
```

## Database Schema

### Updated User Model

```sql
CREATE TABLE user (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR(20) DEFAULT 'student',  -- 'student' or 'teacher'
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE
);
```

### Assignment Model

```sql
CREATE TABLE assignment (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    student_id UUID REFERENCES user(id) ON DELETE CASCADE,
    teacher_id UUID REFERENCES user(id) ON DELETE SET NULL,
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INTEGER NOT NULL,
    uploaded_at TIMESTAMP NOT NULL,
    graded_at TIMESTAMP,
    grade FLOAT,
    status VARCHAR(20) DEFAULT 'pending',  -- 'pending' or 'graded'
    comments VARCHAR(1000)
);
```

## File Storage

Uploaded files are stored in:
```
backend/uploads/assignments/
```

Files are automatically:
- Validated for type and size
- Renamed with UUIDs to prevent conflicts
- Associated with the uploading student

### File Restrictions

- **Allowed types**: PDF, DOC, DOCX, ZIP, JPG, JPEG, PNG, TXT
- **Max size**: 10 MB

## API Endpoints

All endpoints are under `/api/v1/assignments/`:

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| POST | `/upload` | Student | Upload a new assignment |
| GET | `/my` | All | Get assignments (filtered by role) |
| GET | `/all` | Teacher | Get all assignments |
| PUT | `/{id}/grade` | Teacher | Grade an assignment |
| GET | `/{id}/download` | All | Download assignment file |
| GET | `/stats` | All | Get statistics |
| DELETE | `/{id}` | All | Delete assignment |

See `ASSIGNMENT_API_DOCS.md` for detailed documentation.

## User Roles

### Teacher (`teacher1`)
- View all student assignments
- Download any assignment file
- Grade assignments
- View overall statistics
- Cannot upload assignments

### Students (`user1` - `user10`)
- Upload assignments
- View only their own assignments
- Download their own files
- View their own statistics
- Cannot grade assignments
- Cannot view other students' work

## Security Features

1. **JWT Authentication** - All endpoints require valid tokens
2. **Role-based Access Control** - Automatic permission checks
3. **File Type Validation** - Only allowed file types accepted
4. **File Size Limits** - Maximum 10 MB per file
5. **Secure File Naming** - UUIDs prevent path traversal
6. **Database Relationships** - CASCADE delete for data integrity

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── api_v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── assignments.py  # Assignment endpoints
│   │   │   │   └── btec.py
│   │   │   └── api.py
│   │   ├── deps.py                  # Role dependencies
│   │   └── main.py
│   ├── alembic/
│   │   └── versions/
│   │       └── a1b2c3d4e5f6_*.py   # Migration file
│   ├── core/
│   │   ├── config.py
│   │   ├── db.py                    # Initial data setup
│   │   └── security.py
│   ├── crud.py                      # CRUD operations
│   ├── models.py                    # User & Assignment models
│   └── main.py
├── uploads/
│   └── assignments/                 # Uploaded files
└── alembic.ini
```

## Troubleshooting

### Database Connection Error
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check .env file has correct credentials
cat .env
```

### Migration Errors
```bash
# Reset migrations (WARNING: Deletes all data)
alembic downgrade base
alembic upgrade head

# Or manually run SQL
psql -U postgres -d app -f reset_db.sql
```

### Import Errors
```bash
# Make sure PYTHONPATH is set
export PYTHONPATH=/path/to/backend:$PYTHONPATH

# Install missing dependencies
pip install python-multipart
```

## Development

### Adding New Endpoints

1. Add endpoint function in `app/api/api_v1/endpoints/assignments.py`
2. Use `TeacherUser` or `StudentUser` dependency for role-based access
3. Update `ASSIGNMENT_API_DOCS.md`

### Modifying Models

1. Update model in `app/models.py`
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Apply migration: `alembic upgrade head`

## Production Deployment

1. **Update Environment Variables**:
   - Change `SECRET_KEY`
   - Use strong passwords
   - Set `ENVIRONMENT=production`

2. **Use Production Database**:
   - PostgreSQL in production mode
   - Enable SSL connections
   - Regular backups

3. **File Storage**:
   - Consider using cloud storage (S3, etc.)
   - Implement file cleanup policies
   - Add virus scanning

4. **Security**:
   - Enable HTTPS
   - Add rate limiting
   - Implement file quarantine
   - Add logging and monitoring

## Next Steps

1. ✅ Core functionality implemented
2. 🔄 Add frontend UI (Optional)
3. 🔄 Add email notifications
4. 🔄 Add file preview capabilities
5. 🔄 Add bulk grading features
6. 🔄 Add export to CSV/Excel
7. 🔄 Add assignment deadlines
8. 🔄 Add file versioning

## Support

For issues or questions:
1. Check `ASSIGNMENT_API_DOCS.md` for API usage
2. Run `python test_assignment_api.py` for component validation
3. Check server logs for errors
4. Review migration files for schema details
