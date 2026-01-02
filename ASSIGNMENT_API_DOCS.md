# Assignment Management API Documentation

This document describes the Assignment Management System API endpoints for file uploads and grading.

## Overview

The system supports two user roles:
- **Teacher** (`teacher1`): Can view all assignments, grade them, and download files
- **Student** (`user1` to `user10`): Can upload assignments, view their own submissions, and check grades

All users have the password: `1234`

## Authentication

All endpoints require authentication using JWT tokens. First, obtain a token by logging in.

### Login
```bash
# Login as teacher
curl -X POST "http://localhost/api/v1/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teacher1@btec.edu&password=1234"

# Login as student
curl -X POST "http://localhost/api/v1/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user1@btec.edu&password=1234"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Use the token in subsequent requests:
```bash
export TOKEN="your_access_token_here"
```

## API Endpoints

### 1. Upload Assignment (Student Only)

Upload a new assignment with a file.

**Endpoint:** `POST /api/v1/assignments/upload`

**Required Role:** Student

**Parameters:**
- `title` (form): Assignment title (required)
- `description` (form): Assignment description (optional)
- `file` (file): The file to upload (required)

**Allowed file types:** `.pdf`, `.doc`, `.docx`, `.zip`, `.jpg`, `.jpeg`, `.png`, `.txt`

**Max file size:** 10 MB

**Example:**
```bash
curl -X POST "http://localhost/api/v1/assignments/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "title=Math Homework Week 1" \
  -F "description=Algebra exercises from chapter 3" \
  -F "file=@/path/to/homework.pdf"
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Math Homework Week 1",
  "description": "Algebra exercises from chapter 3",
  "student_id": "student-uuid",
  "teacher_id": null,
  "file_name": "homework.pdf",
  "file_size": 245678,
  "uploaded_at": "2026-01-02T20:30:00",
  "graded_at": null,
  "grade": null,
  "status": "pending",
  "comments": null
}
```

### 2. Get My Assignments

Retrieve assignments for the current user.
- Students see only their own assignments
- Teachers see all assignments

**Endpoint:** `GET /api/v1/assignments/my`

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 100)

**Example:**
```bash
# Student request
curl -X GET "http://localhost/api/v1/assignments/my?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"

# Teacher request (gets all assignments)
curl -X GET "http://localhost/api/v1/assignments/my?skip=0&limit=10" \
  -H "Authorization: Bearer $TEACHER_TOKEN"
```

**Response:**
```json
{
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Math Homework Week 1",
      "description": "Algebra exercises from chapter 3",
      "student_id": "student-uuid",
      "teacher_id": null,
      "file_name": "homework.pdf",
      "file_size": 245678,
      "uploaded_at": "2026-01-02T20:30:00",
      "graded_at": null,
      "grade": null,
      "status": "pending",
      "comments": null
    }
  ],
  "count": 1
}
```

### 3. Get All Assignments (Teacher Only)

Retrieve all assignments from all students.

**Endpoint:** `GET /api/v1/assignments/all`

**Required Role:** Teacher

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 100)

**Example:**
```bash
curl -X GET "http://localhost/api/v1/assignments/all?skip=0&limit=50" \
  -H "Authorization: Bearer $TEACHER_TOKEN"
```

### 4. Grade Assignment (Teacher Only)

Add a grade and comments to an assignment.

**Endpoint:** `PUT /api/v1/assignments/{assignment_id}/grade`

**Required Role:** Teacher

**Parameters:**
- `grade` (form): Grade value 0-100 (required)
- `comments` (form): Teacher's comments (optional)

**Example:**
```bash
curl -X PUT "http://localhost/api/v1/assignments/123e4567-e89b-12d3-a456-426614174000/grade" \
  -H "Authorization: Bearer $TEACHER_TOKEN" \
  -F "grade=85.5" \
  -F "comments=Good work! Pay attention to problem 5."
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Math Homework Week 1",
  "description": "Algebra exercises from chapter 3",
  "student_id": "student-uuid",
  "teacher_id": "teacher-uuid",
  "file_name": "homework.pdf",
  "file_size": 245678,
  "uploaded_at": "2026-01-02T20:30:00",
  "graded_at": "2026-01-02T21:00:00",
  "grade": 85.5,
  "status": "graded",
  "comments": "Good work! Pay attention to problem 5."
}
```

### 5. Download Assignment File

Download the file attached to an assignment.
- Students can only download their own files
- Teachers can download any file

**Endpoint:** `GET /api/v1/assignments/{assignment_id}/download`

**Example:**
```bash
# Download and save to file
curl -X GET "http://localhost/api/v1/assignments/123e4567-e89b-12d3-a456-426614174000/download" \
  -H "Authorization: Bearer $TOKEN" \
  -o downloaded_file.pdf
```

### 6. Get Assignment Statistics

Get statistics about assignments.
- Students see their own statistics
- Teachers see overall statistics

**Endpoint:** `GET /api/v1/assignments/stats`

**Example:**
```bash
# Student statistics
curl -X GET "http://localhost/api/v1/assignments/stats" \
  -H "Authorization: Bearer $TOKEN"

# Teacher statistics (all students)
curl -X GET "http://localhost/api/v1/assignments/stats" \
  -H "Authorization: Bearer $TEACHER_TOKEN"
```

**Response:**
```json
{
  "total_assignments": 15,
  "pending_assignments": 3,
  "graded_assignments": 12,
  "average_grade": 87.5
}
```

### 7. Delete Assignment

Delete an assignment and its associated file.
- Students can only delete their own assignments
- Teachers can delete any assignment

**Endpoint:** `DELETE /api/v1/assignments/{assignment_id}`

**Example:**
```bash
curl -X DELETE "http://localhost/api/v1/assignments/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "message": "Assignment deleted successfully"
}
```

## User Roles and Permissions

| Action | Student | Teacher |
|--------|---------|---------|
| Upload assignment | ✅ | ❌ |
| View own assignments | ✅ | ✅ (all) |
| View all assignments | ❌ | ✅ |
| Grade assignments | ❌ | ✅ |
| Download own files | ✅ | ✅ (all) |
| Delete own assignments | ✅ | ✅ (all) |

## Error Responses

### 400 Bad Request
```json
{
  "detail": "File type not allowed. Allowed types: .pdf, .doc, .docx, .zip, .jpg, .jpeg, .png, .txt"
}
```

### 403 Forbidden
```json
{
  "detail": "Only teachers can access this resource"
}
```

### 404 Not Found
```json
{
  "detail": "Assignment not found"
}
```

## Testing Workflow

### As a Student:
1. Login to get access token
2. Upload an assignment
3. View your assignments
4. Check statistics
5. Download your file (if needed)

### As a Teacher:
1. Login to get access token
2. View all assignments
3. Grade pending assignments
4. Download student files
5. Check overall statistics

## Database Schema

### User Table
- `id`: UUID (Primary Key)
- `email`: String (Unique)
- `username`: String (Unique)
- `hashed_password`: String
- `role`: String (`student` or `teacher`)
- `full_name`: String
- `is_active`: Boolean
- `is_superuser`: Boolean

### Assignment Table
- `id`: UUID (Primary Key)
- `title`: String
- `description`: String
- `student_id`: UUID (Foreign Key to User)
- `teacher_id`: UUID (Foreign Key to User, nullable)
- `file_path`: String
- `file_name`: String
- `file_size`: Integer
- `uploaded_at`: DateTime
- `graded_at`: DateTime (nullable)
- `grade`: Float (nullable)
- `status`: String (`pending` or `graded`)
- `comments`: String (nullable)

## Initial Users

The system comes pre-configured with test users:

**Teacher:**
- Email: `teacher1@btec.edu`
- Username: `teacher1`
- Password: `1234`
- Role: `teacher`

**Students:**
- Emails: `user1@btec.edu` to `user10@btec.edu`
- Usernames: `user1` to `user10`
- Password: `1234` (all students)
- Role: `student`

## File Storage

Uploaded files are stored in:
```
backend/uploads/assignments/
```

Files are renamed using UUIDs to prevent conflicts and security issues.
