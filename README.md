# BTEC Backend API

A production-ready FastAPI backend with JWT authentication, SQLAlchemy ORM, Alembic migrations, and automated CI/CD deployment to Render.

## Features

- ✅ **FastAPI** - Modern, fast web framework
- ✅ **SQLAlchemy** - Powerful ORM for database management
- ✅ **Alembic** - Database migration management
- ✅ **JWT Authentication** - Secure token-based auth with python-jose
- ✅ **Password Hashing** - Bcrypt password hashing with passlib
- ✅ **CORS Support** - Configurable cross-origin resource sharing
- ✅ **SQLite/PostgreSQL** - SQLite for dev, PostgreSQL for production
- ✅ **Pydantic** - Data validation with Pydantic schemas
- ✅ **Pytest** - Comprehensive test suite
- ✅ **Docker** - Containerized deployment
- ✅ **CI/CD** - Automated testing and deployment with GitHub Actions
- ✅ **Render** - One-click deployment to Render platform

## Quick Start

### Prerequisites

- Python 3.11+
- pip package manager

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kk121288/BTEC-backend.git
   cd BTEC-backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration (default SQLite works out of the box)
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API**
   - API Docs: http://localhost:8000/api/docs
   - Health Check: http://localhost:8000/api/health

## API Endpoints

### Health Check
- `GET /api/health` - Health check endpoint

### Authentication
- `POST /api/auth/register` - Register a new user
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
  }
  ```

- `POST /api/auth/login` - Login and get access token
  ```json
  {
    "username": "user@example.com",
    "password": "securepassword"
  }
  ```

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback last migration:
```bash
alembic downgrade -1
```

## Docker

Build the Docker image:
```bash
docker build -t btec-backend .
```

Run the container:
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./dev.db \
  -e SECRET_KEY=your-secret-key \
  btec-backend
```

## Deployment to Render

### Prerequisites
1. Create a [Render](https://render.com) account
2. Create a new PostgreSQL database
3. Create a new Web Service

### Setup Steps

1. **Connect your GitHub repository** to Render

2. **Configure environment variables** in Render dashboard:
   - `DATABASE_URL` - Auto-filled from PostgreSQL database
   - `SECRET_KEY` - Generate with `openssl rand -hex 32`
   - `ALGORITHM` - Set to `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES` - Set to `11520` (8 days)
   - `BACKEND_CORS_ORIGINS` - Set to `["*"]` or your frontend URLs

3. **Deploy** - Render will automatically deploy on push to main branch

### GitHub Secrets (for CI/CD)

Add these secrets to your GitHub repository settings:
- `RENDER_API_KEY` - Your Render API key
- `RENDER_SERVICE_ID` - Your Render service ID

See `.secrets_placeholders.md` for detailed instructions.

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── core/
│   │   ├── config.py           # Settings and configuration
│   │   └── security.py         # JWT and password utilities
│   ├── db/
│   │   └── session.py          # Database session management
│   ├── models/
│   │   └── user.py             # SQLAlchemy models
│   ├── schemas/
│   │   └── user.py             # Pydantic schemas
│   ├── crud/
│   │   └── user.py             # CRUD operations
│   └── api/
│       ├── deps.py             # Dependencies
│       └── routes/
│           ├── auth.py         # Authentication endpoints
│           └── health.py       # Health check endpoint
├── alembic/
│   ├── versions/               # Migration files
│   ├── env.py                  # Alembic environment
│   └── script.py.mako          # Migration template
├── tests/
│   ├── conftest.py             # Test fixtures
│   └── test_auth.py            # Authentication tests
├── .github/
│   └── workflows/
│       ├── lint.yml            # Code linting
│       ├── test.yml            # Run tests
│       ├── build.yml           # Build Docker image
│       └── deploy-render.yml   # Deploy to Render
├── Dockerfile                  # Docker configuration
├── render.yaml                 # Render configuration
├── requirements.txt            # Python dependencies
├── alembic.ini                 # Alembic configuration
└── .env.example                # Environment variables template
```

## Development Workflow

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Run tests: `pytest tests/ -v`
4. Run linting: `ruff check app/ tests/`
5. Commit changes: `git commit -m "Add my feature"`
6. Push to GitHub: `git push origin feature/my-feature`
7. Create a Pull Request
8. CI/CD will automatically run tests and linting
9. After merge to main, automatic deployment to Render

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/kk121288/BTEC-backend/issues
- Documentation: See `/api/docs` when running the server

## Next Steps

- [ ] Add user profile endpoints
- [ ] Implement password reset functionality
- [ ] Add email verification
- [ ] Implement role-based access control (RBAC)
- [ ] Add API rate limiting
- [ ] Set up monitoring with Sentry
- [ ] Add more comprehensive tests
- [ ] Create admin dashboard

---

Built with ❤️ using FastAPI
