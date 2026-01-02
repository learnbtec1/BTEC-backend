# MetaLearn Pro - API Services Documentation

## 🌐 Service Architecture

MetaLearn Pro is built on a microservices architecture with the following independent services:

### Core Services

| Service | Port | Description | Status |
|---------|------|-------------|--------|
| **Backend API** | 8000 | Main application API and gateway | ✅ Implemented |
| **AI Tutor** | 8001 | Intelligent virtual tutor | ✅ Implemented |
| **Learning Companion** | 8002 | Personal learning assistant | ✅ Implemented |
| **Gamification** | 8003 | Points, badges, and rewards | ✅ Implemented |
| **Virtual Campus** | 8004 | VR classrooms and labs | ✅ Implemented |
| **Analytics** | 8005 | Performance analytics & reporting | ✅ Implemented |
| **Simulations** | 8006 | Interactive simulations | ✅ Implemented |
| **Blockchain** | 8007 | Certificate management | ✅ Implemented |

---

## 📡 API Endpoints by Service

### 1. AI Tutor Service (Port 8001)

**Base URL:** `http://localhost:8001`

#### Endpoints:
- `POST /api/v1/assess-level` - Assess student level
- `POST /api/v1/feedback` - Get instant feedback on answers
- `GET /api/v1/adaptive-path/{student_id}` - Get adaptive learning path
- `POST /api/v1/diagnose` - Intelligent diagnosis of strengths/weaknesses
- `POST /api/v1/emotional-support` - Sentiment analysis and emotional support

**Key Features:**
- Automatic student level assessment
- Adaptive learning content adjustment
- Instant feedback mechanism
- Personalized recommendations
- Emotional support with sentiment analysis

---

### 2. Learning Companion Service (Port 8002)

**Base URL:** `http://localhost:8002`

#### Endpoints:
- `POST /api/v1/reminders` - Create smart reminder
- `GET /api/v1/reminders/{student_id}` - Get student reminders
- `GET /api/v1/performance/{student_id}` - Analyze performance
- `GET /api/v1/performance-chart/{student_id}` - Get performance charts
- `GET /api/v1/predict-outcome/{student_id}` - Predict outcomes
- `GET /api/v1/recommendations/{student_id}` - Get dynamic recommendations
- `GET /api/v1/study-plan/{student_id}` - Get adjusted study plan
- `POST /api/v1/study-plan/{student_id}/adjust` - Adjust study plan

**Key Features:**
- Smart scheduling and reminders
- Performance analytics with charts
- Outcome prediction
- Dynamic recommendations
- Automatic study plan adjustment

---

### 3. Gamification Engine (Port 8003)

**Base URL:** `http://localhost:8003`

#### Endpoints:
- `GET /api/v1/points/{student_id}` - Get student points
- `POST /api/v1/points/{student_id}/add` - Add points
- `GET /api/v1/badges/{student_id}` - Get student badges
- `GET /api/v1/level/{student_id}` - Get student level
- `GET /api/v1/challenges/{student_id}` - Get challenges
- `GET /api/v1/leaderboard` - Get leaderboard
- `GET /api/v1/avatar/{student_id}` - Get student avatar
- `POST /api/v1/avatar/{student_id}/customize` - Customize avatar
- `GET /api/v1/rewards` - Get available rewards

**Key Features:**
- Points and badges system
- Levels and challenges
- Leaderboards
- Daily quests
- Avatar customization
- Educational rewards

---

### 4. Virtual Campus Service (Port 8004)

**Base URL:** `http://localhost:8004`

#### Endpoints:
- `GET /api/v1/classrooms` - Get virtual classrooms
- `GET /api/v1/labs` - Get virtual labs
- `GET /api/v1/library` - Get smart library
- `GET /api/v1/lecture-theaters` - Get lecture theaters
- `GET /api/v1/collaboration-zones` - Get collaboration spaces
- `GET /api/v1/historical-worlds` - Get historical worlds
- `GET /api/v1/scientific-worlds` - Get scientific worlds
- `POST /api/v1/join-room` - Join virtual room
- `POST /api/v1/leave-room` - Leave virtual room

**Key Features:**
- Smart interactive classrooms
- Virtual labs (chemistry, physics, programming)
- Smart digital library
- Lecture theaters
- Collaboration zones
- Historical world exploration
- Scientific world exploration

---

### 5. Analytics & Reporting (Port 8005)

**Base URL:** `http://localhost:8005`

#### Endpoints:
- `GET /api/v1/student-analytics/{student_id}` - Student performance analysis
- `GET /api/v1/class-statistics/{class_id}` - Class statistics
- `GET /api/v1/teacher-report/{teacher_id}` - Teacher performance report
- `GET /api/v1/performance-chart/{entity_id}` - Performance charts
- `GET /api/v1/predict-grade/{student_id}` - Predict final grade
- `GET /api/v1/engagement-metrics/{student_id}` - Engagement metrics
- `POST /api/v1/compare` - Comparative analysis
- `GET /api/v1/export-report/{report_type}` - Export reports

**Key Features:**
- Student performance analysis
- Class-level statistics
- Teacher performance reports
- Grade prediction
- Interactive charts
- Comparative analysis
- Report export (PDF, Excel, CSV)

---

### 6. Interactive Simulations (Port 8006)

**Base URL:** `http://localhost:8006`

#### Endpoints:
- `GET /api/v1/simulations` - Get all simulations
- `GET /api/v1/chemistry-lab/{experiment_id}` - Chemistry experiment
- `GET /api/v1/surgery/{simulation_id}` - Surgery simulation
- `GET /api/v1/space/{simulation_id}` - Space simulation
- `POST /api/v1/start-simulation` - Start simulation
- `POST /api/v1/complete-simulation` - Complete simulation
- `GET /api/v1/leaderboard/{simulation_id}` - Simulation leaderboard

**Key Features:**
- Virtual chemistry lab
- Virtual surgery simulator
- Space simulation
- Engineering construction
- Virtual courtroom
- Real-time performance tracking

---

### 7. Blockchain Certificates (Port 8007)

**Base URL:** `http://localhost:8007`

#### Endpoints:
- `POST /api/v1/issue-certificate` - Issue blockchain certificate
- `POST /api/v1/mint-nft` - Mint NFT certificate
- `GET /api/v1/verify/{certificate_id}` - Verify certificate
- `GET /api/v1/student-record/{student_id}` - Educational record
- `GET /api/v1/certificates/{student_id}` - Get student certificates
- `POST /api/v1/revoke-certificate` - Revoke certificate
- `GET /api/v1/blockchain-stats` - Blockchain statistics
- `POST /api/v1/batch-issue` - Batch issue certificates

**Key Features:**
- Tamper-proof certificates
- NFT certificates
- Permanent educational record
- Certificate verification
- IPFS storage
- Multi-blockchain support (Ethereum, Polygon)

---

## 🔗 Service Communication

All microservices communicate through:
- **REST APIs** for synchronous communication
- **Redis** for caching and pub/sub
- **PostgreSQL** for shared data persistence

---

## 🔐 Authentication & Authorization

All services support:
- JWT token authentication
- API key authentication
- Role-based access control (Student, Teacher, Parent, Admin)

---

## 📊 Monitoring & Health Checks

Each service provides:
- Health check endpoint at root (`/`)
- Metrics endpoint
- OpenAPI documentation at `/docs`
- ReDoc documentation at `/redoc`

---

## 🚀 Quick Start

### Using Docker Compose
```bash
docker-compose -f docker-compose.metalearn.yml up -d
```

### Individual Service
```bash
cd services/ai_tutor
pip install -r requirements.txt
python main.py
```

---

## 📖 Documentation Links

- **OpenAPI/Swagger**: `http://localhost:{port}/docs`
- **ReDoc**: `http://localhost:{port}/redoc`
- **Health Check**: `http://localhost:{port}/`

---

## 🌍 Language Support

All services support bilingual responses:
- **Arabic (العربية)** - RTL support
- **English** - LTR support

---

## 📞 Support

For API support and questions:
- Email: api@metalearnpro.com
- Discord: [MetaLearn Pro Community](https://discord.gg/metalearnpro)
- GitHub Issues: [Report an issue](https://github.com/kk121288/BTEC-backend/issues)
