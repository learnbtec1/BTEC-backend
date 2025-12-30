# 🧪 End-to-End Testing Guide

## Overview
This guide walks through complete end-to-end testing of the BTEC Smart Platform, from backend setup to frontend interaction.

---

## Prerequisites

Before running tests, ensure you have:
- ✅ Python 3.11+
- ✅ UV package manager
- ✅ Flutter 3.0+
- ✅ PostgreSQL 15+ (optional for full testing)

---

## Quick Test Setup

### Option 1: Automated (Recommended)

```bash
# Run the quick deploy script
./quick-deploy.sh

# Choose option 1 (Local Development)
# The script will:
# - Check prerequisites
# - Install UV if needed
# - Set up backend dependencies
# - Set up Flutter dependencies
# - Create .env from .env.example (if not exists)
```

### Option 2: Manual Setup

```bash
# 1. Create .env file
cp .env.example .env

# 2. Backend setup
cd backend
uv sync
cd ..

# 3. Frontend setup
cd Flutter
flutter pub get
cd ..
```

---

## Test Scenarios

### 1️⃣ Backend Health Check

**Objective**: Verify backend starts without errors

```bash
cd backend

# Start backend
uv run fastapi dev app/main.py

# Expected output:
# ✅ INFO:     Uvicorn running on http://127.0.0.1:8000
# ✅ INFO:     Application startup complete
```

**Test the health endpoint:**
```bash
# In a new terminal
curl http://localhost:8000/api/v1/health

# Expected: {"status": "ok"} or similar
```

**✅ Pass Criteria**: Backend starts without errors, health endpoint responds

---

### 2️⃣ Text Evaluation API

**Objective**: Test text similarity evaluation

```bash
# Backend should be running from Test 1

curl -X POST http://localhost:8000/api/v1/btec/evaluate/text \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "student_answer=The quick brown fox&model_answer=The quick brown fox jumps"
```

**Expected Response:**
```json
{
  "status": "ok",
  "data": {
    "similarity": 0.85,
    "levenshtein_ratio": 0.78
  }
}
```

**✅ Pass Criteria**: 
- Response status 200
- Contains similarity score (0-1)
- Contains levenshtein_ratio (0-1)

---

### 3️⃣ Audio Transcription (Whisper)

**Objective**: Test audio-to-text conversion

**Note**: This test requires a valid audio file and internet connection for Whisper model download (first time only).

```bash
# Create a test audio file or use an existing one
# For testing, you can record a simple message:
# "Hello, this is a test message"

curl -X POST http://localhost:8000/api/v1/btec/evaluate/audio \
  -F "file=@test_audio.mp3"
```

**Expected Response:**
```json
{
  "status": "ok",
  "transcript": "Hello, this is a test message"
}
```

**✅ Pass Criteria**:
- Response status 200
- Contains transcript field with text

**Troubleshooting**:
- First run will download Whisper model (~150MB for 'base' model)
- Ensure `WHISPER_MODEL` env var is set (default: 'base')
- Supported formats: mp3, wav, m4a, ogg

---

### 4️⃣ Flutter → Backend Integration

**Objective**: Test complete flow from Flutter UI to backend

**Setup:**
```bash
# Terminal 1: Backend (should already be running)
cd backend
uv run fastapi dev app/main.py

# Terminal 2: Flutter
cd Flutter
flutter run -d chrome
```

**Test Steps:**

1. **Login Screen Test**
   - ✅ App opens to login screen
   - ✅ UI displays correctly with Cairo font
   - ✅ Can enter email/password
   - ✅ Login button works
   - ✅ Navigates to dashboard

2. **Dashboard Test**
   - ✅ Dashboard loads with 4 navigation items
   - ✅ Grid cards display (Text Assessment, Audio, Results, Settings)
   - ✅ Navigation bar switches screens
   - ✅ All icons and text render correctly

3. **Assessment Screen Test**
   - ✅ Navigate to Assessment tab
   - ✅ Text input field works
   - ✅ Enter sample text: "The quick brown fox jumps over the lazy dog"
   - ✅ Click "تقييم الإجابة" (Evaluate Answer) button
   - ✅ Loading indicator shows
   - ✅ Results card appears after ~2 seconds
   - ✅ Shows percentage score and status

4. **Results Screen Test**
   - ✅ Navigate to Results tab
   - ✅ List of assessments displays
   - ✅ Each item shows date and score
   - ✅ Can tap items for details

5. **Settings Screen Test**
   - ✅ Navigate to Settings tab
   - ✅ Profile option visible
   - ✅ Notifications toggle works
   - ✅ Language option shows
   - ✅ Logout option visible

**✅ Pass Criteria**: All UI elements render, navigation works, no console errors

---

### 5️⃣ Full Integration Test

**Objective**: Complete user journey from login to results

**Scenario**: Student evaluates a text answer

1. **Start both services:**
   ```bash
   # Terminal 1: Backend
   cd backend && uv run fastapi dev app/main.py
   
   # Terminal 2: Frontend
   cd Flutter && flutter run -d chrome
   ```

2. **User Actions:**
   - Open app → Login screen
   - Enter credentials → Click login
   - Dashboard loads → Click Assessment
   - Enter text answer
   - Click evaluate
   - View results
   - Navigate to Results tab
   - See history

3. **Expected Flow:**
   ```
   Login → Dashboard → Assessment → [API Call] → Results Display
   ```

4. **Verify:**
   - ✅ No console errors in browser
   - ✅ No exceptions in backend logs
   - ✅ API calls show in network tab
   - ✅ Responses are valid JSON
   - ✅ UI updates after API response

**✅ Pass Criteria**: Complete flow works without errors

---

### 6️⃣ Docker Deployment Test

**Objective**: Verify Docker setup works

```bash
# Copy env file
cp .env.example .env

# Edit .env with your settings
nano .env

# Build and run with Docker
docker-compose -f docker-compose.prod.yml up --build

# Wait for services to start (may take a few minutes)
```

**Test endpoints:**
```bash
# Frontend
curl http://localhost/

# Backend
curl http://localhost:8000/api/v1/health

# Database (should be internal only)
# psql -h localhost -U btec_user -d btec_db
```

**✅ Pass Criteria**:
- All containers start successfully
- Frontend accessible on port 80
- Backend accessible on port 8000
- No errors in `docker-compose logs`

---

## Common Issues & Solutions

### Issue 1: Backend fails to start
**Error**: `ModuleNotFoundError: No module named 'textdistance'`

**Solution**:
```bash
cd backend
uv sync  # Re-sync dependencies
```

### Issue 2: Whisper model download fails
**Error**: `URLError: [Errno -5] No address associated with hostname`

**Solution**:
- Check internet connection
- Set proxy if needed
- Or download model manually and set path in env

### Issue 3: Flutter build fails
**Error**: `Target of URI doesn't exist`

**Solution**:
```bash
cd Flutter
flutter clean
flutter pub get
flutter run -d chrome
```

### Issue 4: CORS errors in browser
**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:
- Check `BACKEND_CORS_ORIGINS` in `.env`
- Ensure includes `http://localhost:5173`
- Restart backend after changing `.env`

### Issue 5: Database connection fails
**Error**: `could not connect to server`

**Solution**:
- Ensure PostgreSQL is running
- Check `POSTGRES_SERVER` in `.env`
- For local dev, can skip DB (app will use defaults)

---

## Performance Benchmarks

Expected performance for reference:

| Operation | Expected Time |
|-----------|--------------|
| Backend startup | < 5 seconds |
| Flutter hot reload | < 1 second |
| Text evaluation | < 500ms |
| Audio transcription (base) | 2-5 seconds |
| Docker build (first time) | 5-10 minutes |
| Docker build (cached) | 1-2 minutes |

---

## Test Checklist

Use this checklist to track your testing:

- [ ] Backend starts without errors
- [ ] Health endpoint responds
- [ ] Text evaluation API works
- [ ] Audio transcription works (optional)
- [ ] Flutter app builds and runs
- [ ] Login screen displays correctly
- [ ] Dashboard navigation works
- [ ] Assessment screen functional
- [ ] Results screen displays
- [ ] Settings screen accessible
- [ ] Full user journey completes
- [ ] Docker deployment works (optional)
- [ ] No console errors
- [ ] No backend exceptions
- [ ] API responses valid

---

## Automated Testing (Future)

To add automated tests:

### Backend:
```bash
cd backend
uv run pytest tests/
```

### Frontend:
```bash
cd Flutter
flutter test
```

**Note**: Test infrastructure is ready but individual test files need to be created.

---

## Next Steps After Testing

Once all tests pass:

1. **For Development**:
   - Continue building features
   - Add more endpoints
   - Enhance UI

2. **For Production**:
   - Follow `DEPLOYMENT_INSTRUCTIONS.md`
   - Choose deployment platform (Render/Railway/Azure)
   - Set production environment variables
   - Deploy!

---

## Support

If you encounter issues during testing:

1. Check `PROJECT_COMPLETION_REPORT.md` for troubleshooting
2. Review `DEPLOYMENT_INSTRUCTIONS.md` for setup help
3. Check GitHub Issues
4. Review backend logs: `uv run fastapi dev app/main.py --log-level debug`

---

**✅ Testing Complete? You're ready to deploy!**

See `DEPLOYMENT_INSTRUCTIONS.md` for production deployment.
