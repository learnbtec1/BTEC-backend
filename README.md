# BTEC Assessment Engine

Educational assessment platform with AI integration.

## 📊 Project Status

**🎯 Overall Progress: 70% Complete**

For detailed project status information:
- **[STATUS.md](./STATUS.md)** - Comprehensive bilingual project status report (English/Arabic)
- **[QUICK_STATUS_AR.md](./QUICK_STATUS_AR.md)** - Quick status summary in Arabic (ملخص سريع بالعربية)
- **[PROJECT_PLAN.md](./PROJECT_PLAN.md)** - Complete 17-phase project plan (Arabic)

### Quick Status Summary

✅ **What's Working:**
- FastAPI backend with PostgreSQL database
- AI evaluation engine (text + audio transcription)
- Flutter frontend with beautiful UI
- JWT authentication system
- Comprehensive CI/CD (20+ workflows)
- Docker containerization

🔄 **In Progress:**
- GPT-4 integration for BTEC grading
- Flutter-Backend integration
- BTEC-specific evaluation logic

📋 **Planned:**
- 3D simulation interface
- PWA features
- Complete notification system

## Quick Start

### Backend
```bash
cd backend
uv sync
source .venv/bin/activate
fastapi run app/main.py
```

### Frontend
```bash
cd Flutter
flutter pub get
flutter run
```

## Documentation

- **[STATUS.md](./STATUS.md)** - Project status (bilingual)
- **[QUICK_STATUS_AR.md](./QUICK_STATUS_AR.md)** - Quick summary (Arabic)
- **[PROJECT_PLAN.md](./PROJECT_PLAN.md)** - 17-phase plan (Arabic)
- **[project-documentation.md](./project-documentation.md)** - Detailed docs (Arabic)
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Deployment guide
- **[development.md](./development.md)** - Development guide

## Phases

1. ✅ Project Setup (Complete)
2. 🔄 UI/UX Enhancement (60%)
3. 📋 Simulation Interface (20%)
4. ✅ i18n Support (Complete)
5. ✅ Dashboard & Charts (Complete)
6. 📋 PWA Integration (Planned)
7. ✅ Testing Infrastructure (Complete)
8. 🔄 Login Redesign (50%)
9. 🔄 User Management (40%)
10. 📋 Course Management (20%)
11. 📋 Assignment Workflow (10%)
12. ✅ AI Plagiarism (Complete)
13. ✅ Audio Integration (Complete)
14. 📋 Notifications (Planned)
15. 🔄 Reporting & Export (30%)
16. ✅ Deployment Pipeline (Complete)
17. 🔄 Documentation (70%)

**Legend:** ✅ Complete | �� In Progress | 📋 Planned

## Architecture

This project consists of three main components:

### 1. Backend (FastAPI)
- Modern Python backend with FastAPI
- PostgreSQL 17 database
- AI evaluation engine (text + audio)
- JWT authentication
- RESTful API with OpenAPI docs

### 2. Frontend (Flutter)
- Cross-platform mobile and web app
- Material Design with Cairo font
- Bilingual support (Arabic/English)
- Interactive charts and visualizations
- Responsive design

### 3. Infrastructure
- Docker containerization
- GitHub Actions CI/CD
- Automated testing
- Health monitoring
- Database migrations (Alembic)

## Technology Stack

**Backend:**
- FastAPI 0.114.2+
- Python 3.10+
- PostgreSQL 17
- SQLModel
- Pydantic
- UV package manager

**Frontend:**
- Flutter 3.0+
- Dart
- Material Design
- Google Fonts
- FL Chart

**AI/ML:**
- OpenAI GPT-4 (in development)
- Whisper API (audio transcription)
- Text similarity algorithms

**DevOps:**
- Docker & Docker Compose
- GitHub Actions
- Pytest
- Alembic migrations

## Contributing

This is an educational research project. Follow existing patterns and maintain code quality.

## License

See [LICENSE](./LICENSE) file for details.
