# Phase 3: AR-Ready Smart Content & Virtual Tutor

## Overview

This phase adds augmented reality support and an intelligent virtual tutor system that provides personalized learning recommendations based on student progress.

## New Features

### 1. AR Model Support

Items now support AR model URLs for augmented reality experiences:

```python
from app.models import ItemCreate

item = ItemCreate(
    title="3D Engine Model",
    description="Interactive 3D car engine",
    ar_model_url="https://example.com/models/engine.glb"
)
```

### 2. Student Progress Tracking

Track student progress across modules with detailed metrics:

```python
from app.models import StudentProgressCreate
from app import crud

progress = StudentProgressCreate(
    module_name="Introduction to Python",
    progress=75,  # 0-100
    struggling=False,
    last_score=82.5,
    attempts=3
)

student_progress = crud.create_or_update_student_progress(
    session=db,
    user_id=user.id,
    progress_in=progress
)
```

### 3. Virtual Tutor Recommendations

The virtual tutor analyzes student progress and provides personalized recommendations:

```python
from app.virtual_tutor import recommend_remediation

recommendations = recommend_remediation(
    session=db,
    user=current_user,
    threshold=60  # Progress threshold
)
```

Each recommendation includes:
- **module_name**: The struggling module
- **current_progress**: Student's progress percentage
- **last_score**: Most recent assessment score
- **attempts**: Number of attempts made
- **struggling**: Whether marked as struggling
- **recommended_action**: Specific guidance based on progress
- **resources**: List of recommended learning resources

### 4. API Endpoints

#### Get Tutor Recommendations

**GET** `/api/v1/tutor/recommendations`

Query Parameters:
- `threshold` (optional, default: 60): Progress percentage below which modules are considered struggling

Response:
```json
{
  "data": [
    {
      "module_name": "Advanced Python",
      "current_progress": 45,
      "last_score": 42.5,
      "attempts": 3,
      "struggling": true,
      "recommended_action": "Focus on core topics and complete practice exercises",
      "resources": [
        "Review video tutorials for this module",
        "Complete interactive practice problems",
        "Access supplementary reading materials"
      ]
    }
  ],
  "count": 1
}
```

## Database Models

### StudentProgress

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| user_id | UUID | Foreign key to User |
| module_name | String(255) | Name of the module |
| progress | Integer (0-100) | Progress percentage |
| struggling | Boolean | Whether student is struggling |
| last_score | Float (0-100) | Most recent score |
| attempts | Integer | Number of attempts |

### Item (Updated)

Added field:
- `ar_model_url`: Optional string (max 2048 chars) for AR model URL

## CRUD Operations

### StudentProgress CRUD

All CRUD operations available in `app/crud.py`:

- `get_student_progress_for_user(session, user_id)` - Get all progress for a user
- `get_student_progress_by_module(session, user_id, module_name)` - Get specific module progress
- `create_or_update_student_progress(session, user_id, progress_in)` - Create or update progress
- `set_student_progress_fields(session, progress_obj, progress_update)` - Update specific fields
- `get_struggling_modules_for_user(session, user_id, progress_threshold)` - Get struggling modules

## Migrations

Migration file: `a1b2c3d4e5f6_add_ar_support_and_studentprogress.py`

To apply migration:
```bash
cd backend
alembic upgrade head
```

To rollback:
```bash
alembic downgrade -1
```

## Testing

### Run All Tests

```bash
cd backend
python -m pytest tests/crud/test_student_progress.py tests/crud/test_virtual_tutor.py tests/api/routes/test_tutor_simple.py -v
```

### Test Coverage

- **StudentProgress CRUD**: 8 comprehensive tests
- **Virtual Tutor Logic**: 10 tests covering various scenarios
- **API Endpoints**: 3 integration tests

All tests passing: ✅ 21/21

### Test Categories

1. **CRUD Tests** (`test_student_progress.py`):
   - Create, read, update operations
   - Module-specific queries
   - User isolation
   - Threshold filtering

2. **Virtual Tutor Tests** (`test_virtual_tutor.py`):
   - Recommendation generation
   - Different progress levels
   - Custom thresholds
   - Resource allocation
   - Multiple module handling

3. **API Tests** (`test_tutor_simple.py`):
   - Endpoint availability
   - Parameter validation
   - Response structure

## Recommendation Logic

The virtual tutor uses a tiered approach based on progress:

| Progress Range | Recommended Action |
|---------------|-------------------|
| < 30% | Review fundamentals and practice basic concepts |
| 30-50% | Focus on core topics and complete practice exercises |
| 50-70% | Work on intermediate concepts and review missed topics |
| 70-100% | Fine-tune understanding with targeted practice |

### Resource Recommendations

Resources are allocated based on:
- **High attempts (>3)**: Tutoring session recommended
- **Low scores (<50)**: Video tutorials and practice problems
- **Low progress (<40)**: Beginner materials and study groups
- **Medium progress (40-70)**: Supplementary materials and examples

## Usage Examples

### Track Student Progress

```python
from sqlmodel import Session
from app import crud
from app.models import StudentProgressCreate

# Create or update progress
progress_in = StudentProgressCreate(
    module_name="Data Structures",
    progress=55,
    struggling=False,
    last_score=58.0,
    attempts=2
)

progress = crud.create_or_update_student_progress(
    session=db,
    user_id=user.id,
    progress_in=progress_in
)
```

### Get Recommendations

```python
from app.virtual_tutor import recommend_remediation

# Get recommendations for struggling modules
recommendations = recommend_remediation(
    session=db,
    user=current_user,
    threshold=60
)

for rec in recommendations:
    print(f"Module: {rec['module_name']}")
    print(f"Action: {rec['recommended_action']}")
    print(f"Resources: {', '.join(rec['resources'])}")
```

### Find Struggling Modules

```python
from app import crud

struggling = crud.get_struggling_modules_for_user(
    session=db,
    user_id=user.id,
    progress_threshold=70  # Custom threshold
)

for module in struggling:
    print(f"{module.module_name}: {module.progress}%")
```

## Architecture

```
┌─────────────────┐
│   API Endpoint  │
│ /tutor/recs     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Virtual Tutor   │
│ recommend_      │
│ remediation()   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CRUD Layer     │
│ get_struggling_ │
│ modules()       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Database      │
│ StudentProgress │
└─────────────────┘
```

## Security Considerations

- The tutor endpoint requires authentication (when full auth is implemented)
- Student progress is isolated by user_id
- Recommendations only include the authenticated user's data
- Input validation on threshold parameter (0-100)

## Future Enhancements

1. **Machine Learning Integration**: Use ML models for smarter recommendations
2. **Learning Path Generation**: Create personalized learning paths
3. **Peer Comparison**: Anonymous benchmarking against peers
4. **Adaptive Thresholds**: Automatically adjust thresholds based on module difficulty
5. **Progress Analytics**: Dashboard with visualizations
6. **Notification System**: Alert students when falling behind

## Dependencies

No new external dependencies added. Uses existing:
- FastAPI
- SQLModel
- SQLAlchemy
- Pydantic

## Performance

- CRUD operations use indexed queries on `user_id` and `module_name`
- Recommendations are computed on-demand (consider caching for production)
- Database queries are optimized with proper indexes on foreign keys

## Troubleshooting

### Tests Fail with Database Connection Error

Make sure you're using SQLite for tests:
```python
# In tests/conftest.py
test_engine = create_engine("sqlite:///./test.db")
```

### Migration Conflicts

If you encounter migration conflicts:
```bash
alembic stamp head
alembic revision --autogenerate -m "your_message"
```

### Import Errors

Ensure all dependencies are installed:
```bash
pip install -e .
```
