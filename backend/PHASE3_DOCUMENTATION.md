# Phase 3: AR-Ready Smart Content & Virtual Tutor Integration

## Overview

This phase adds AR content support and an intelligent virtual tutor system to the BTEC backend. The virtual tutor analyzes student progress across modules and provides personalized remediation recommendations.

## New Features

### 1. AR Model Support for Items

Items now support AR content through the `ar_model_url` field:

```python
from app.models import ItemCreate

item = ItemCreate(
    title="3D Model Example",
    description="Interactive 3D model",
    ar_model_url="https://example.com/models/model.glb"
)
```

### 2. Student Progress Tracking

Track student progress across different learning modules:

```python
from app.models import StudentProgressCreate
from app import crud

# Create or update progress
progress = StudentProgressCreate(
    module_name="Python Basics",
    progress_percentage=75,
    struggling=False,
    last_activity="Completed quiz 3"
)

result = crud.create_or_update_student_progress(
    session=session,
    user_id=user.id,
    progress_in=progress
)
```

### 3. Virtual Tutor Recommendations

Get personalized recommendations based on student performance:

```python
from app.virtual_tutor import recommend_remediation

recommendations = recommend_remediation(
    session=session,
    user=current_user,
    threshold=60  # Progress percentage threshold
)
```

## API Endpoints

### Get Tutor Recommendations

**Endpoint:** `GET /api/v1/tutor/recommendations`

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `threshold` (optional): Progress percentage threshold (0-100, default: 60)

**Example Request:**
```bash
curl -X GET "http://localhost/api/v1/tutor/recommendations?threshold=60" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Example Response:**
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "user_email": "student@example.com",
  "threshold": 60,
  "recommendations": [
    {
      "module_name": "Python Basics",
      "current_progress": 45,
      "struggling": true,
      "recommendations": [
        "Practice intermediate exercises for Python Basics",
        "Review video tutorials for challenging topics",
        "Join a study group for peer learning",
        "Explore AR simulations and 3D models for Python Basics"
      ]
    }
  ]
}
```

## Database Models

### StudentProgress

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `user_id` | UUID | Foreign key to user |
| `module_name` | String(255) | Name of the learning module |
| `progress_percentage` | Integer(0-100) | Current progress percentage |
| `struggling` | Boolean | Flag indicating if student is struggling |
| `last_activity` | String(255) | Description of last activity |

### Item (Updated)

Added field:
- `ar_model_url` (String, max 2048): URL to AR model file

## CRUD Operations

### Student Progress CRUD

```python
from app import crud

# Get all progress for a user
all_progress = crud.get_student_progress_for_user(
    session=session,
    user_id=user.id
)

# Get progress for specific module
module_progress = crud.get_student_progress_by_module(
    session=session,
    user_id=user.id,
    module_name="Python Basics"
)

# Update specific fields
from app.models import StudentProgressUpdate

update = StudentProgressUpdate(
    progress_percentage=80,
    last_activity="Completed assignment"
)

updated = crud.set_student_progress_fields(
    session=session,
    progress_obj=existing_progress,
    progress_update=update
)

# Get struggling modules
struggling = crud.get_struggling_modules_for_user(
    session=session,
    user_id=user.id,
    progress_threshold=60
)
```

## Database Migration

To apply the database changes:

```bash
# Inside the backend container
alembic upgrade head
```

To rollback:

```bash
alembic downgrade -1
```

Migration file: `a1b2c3d4e5f6_add_ar_support_and_studentprogress.py`

This migration:
1. Adds `ar_model_url` column to `item` table
2. Creates `studentprogress` table with proper relationships

## Testing

Run the tests:

```bash
# Inside the backend container
bash scripts/test.sh

# Or run specific test files
pytest tests/crud/test_student_progress.py
pytest tests/utils/test_virtual_tutor.py
pytest tests/api/routes/test_tutor.py
```

## Recommendation Logic

The virtual tutor provides different recommendations based on progress levels:

### Low Progress (< 30%)
- Review fundamental concepts
- Schedule 1-on-1 tutoring
- Complete introductory exercises

### Medium Progress (30-59%)
- Practice intermediate exercises
- Review video tutorials
- Join study groups

### Higher Progress (≥ 60% but marked struggling)
- Focus on advanced topics
- Complete practice problems
- Review errors and misconceptions

All recommendations include AR-specific suggestions when available.

## Security Considerations

- All endpoints require authentication
- Progress data is scoped to the authenticated user
- Foreign key constraints ensure data integrity
- Cascade delete removes progress when user is deleted

## Best Practices

1. **Update Progress Regularly**: Call `create_or_update_student_progress` after each learning activity
2. **Set Struggling Flag**: Mark modules where students need help regardless of percentage
3. **Use Appropriate Thresholds**: Adjust threshold based on course difficulty
4. **Provide Activity Context**: Use `last_activity` to give context for recommendations
5. **Leverage AR Content**: Include AR model URLs for interactive learning experiences

## Future Enhancements

Potential improvements for future phases:
- Machine learning-based recommendations
- Time-based progress analytics
- Peer comparison and collaboration features
- Integration with external learning resources
- Advanced AR content management
