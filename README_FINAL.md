# 🎓 BTEC Smart Platform - منصة التقييم الذكية

<div align="center">

![BTEC Platform](https://img.shields.io/badge/BTEC-Smart%20Platform-blue)
![Flutter](https://img.shields.io/badge/Flutter-3.0%2B-02569B?logo=flutter)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql)

**منصة تقييم ذكية مدعومة بالذكاء الاصطناعي لتحليل الإجابات النصية والصوتية**

[التثبيت](#-التثبيت-السريع) • [المميزات](#-المميزات) • [البنية](#-البنية-التقنية) • [النشر](#-النشر)

</div>

---

## 📋 نظرة عامة

BTEC Smart Platform هي منصة شاملة لتقييم الطلاب باستخدام الذكاء الاصطناعي، مصممة خصيصاً لمعايير BTEC التعليمية.

### ✨ المميزات الرئيسية

#### 🤖 محرك الذكاء الاصطناعي
- **تقييم نصي ذكي**: مقارنة الإجابات باستخدام خوارزميات التشابه المتقدمة
- **تحويل الصوت إلى نص**: دعم كامل لـ OpenAI Whisper
- **كشف الانتحال**: التحقق من أصالة المحتوى
- **تقييم متعدد المعايير**: Cosine Similarity + Levenshtein Distance

#### 📱 واجهة مستخدم حديثة
- **تصميم متجاوب**: يعمل على الويب والموبايل
- **واجهة عربية**: دعم كامل للغة العربية (RTL)
- **تجربة مستخدم سلسة**: انيميشنز وانتقالات سلسة
- **لوحة تحكم شاملة**: عرض النتائج والإحصائيات

#### 🔒 أمان وموثوقية
- **مصادقة JWT**: نظام تسجيل دخول آمن
- **CORS محمي**: إعدادات أمان متقدمة
- **تشفير البيانات**: حماية المعلومات الحساسة
- **Rate Limiting**: حماية من الهجمات

---

## 🚀 التثبيت السريع

### المتطلبات الأساسية
```bash
# Backend
Python 3.11+
PostgreSQL 15+
UV Package Manager

# Frontend
Flutter 3.0+
Dart SDK
```

### 1. استنساخ المشروع
```bash
git clone https://github.com/kk121288/BTEC-backend.git
cd BTEC-backend
```

### 2. إعداد Backend
```bash
cd backend

# تثبيت UV
pip install uv

# مزامنة المكتبات
uv sync

# نسخ ملف البيئة
cp ../.env.example ../.env

# تعديل المتغيرات
nano ../.env

# تشغيل Backend
uv run fastapi dev app/main.py
```

Backend يعمل على: `http://localhost:8000` 🎉

### 3. إعداد Frontend
```bash
cd ../Flutter

# تثبيت المكتبات
flutter pub get

# تشغيل على الويب
flutter run -d chrome

# أو على الموبايل
flutter run
```

Frontend يعمل على: `http://localhost:xxxx` 🎉

---

## 🏗️ البنية التقنية

### Backend Architecture

```
backend/
├── app/
│   ├── api/
│   │   ├── api_v1/
│   │   │   ├── api.py              # API router aggregation
│   │   │   └── endpoints/
│   │   │       └── btec.py         # BTEC evaluation endpoints
│   │   └── main.py                 # Main API router
│   ├── btec_engine/
│   │   ├── text_evaluator.py      # Text similarity engine
│   │   └── audio_evaluator.py     # Whisper integration
│   ├── core/
│   │   ├── config.py               # Settings & environment
│   │   ├── db.py                   # Database connection
│   │   └── security.py             # Auth & JWT
│   └── main.py                     # FastAPI application
└── pyproject.toml                  # Dependencies
```

### Frontend Architecture

```
Flutter/lib/
├── core/
│   ├── constants/
│   │   ├── api_constants.dart      # API configuration
│   │   └── app_constants.dart      # App settings
│   └── network/
│       └── api_client.dart         # HTTP client
├── features/
│   ├── auth/
│   │   ├── models/                 # User models
│   │   ├── screens/                # Login screen
│   │   └── services/               # Auth service
│   ├── dashboard/
│   │   └── screens/                # Dashboard UI
│   ├── assessment/
│   │   ├── models/                 # Assessment models
│   │   ├── screens/                # Assessment UI
│   │   └── services/               # Assessment service
│   ├── results/
│   │   └── screens/                # Results display
│   └── settings/
│       └── screens/                # Settings UI
└── main.dart                       # App entry point
```

---

## 🔌 API Endpoints

### Authentication
```http
POST /api/v1/auth/login
POST /api/v1/auth/register
```

### BTEC Evaluation
```http
POST /api/v1/btec/evaluate/text
Content-Type: application/x-www-form-urlencoded

student_answer=Hello&model_answer=Hello World
```

```http
POST /api/v1/btec/evaluate/audio
Content-Type: multipart/form-data

file: audio.mp3
```

### Results
```http
GET /api/v1/btec/results
```

---

## 🐳 النشر باستخدام Docker

### تشغيل المشروع بالكامل

```bash
# إنشاء ملف .env
cp .env.example .env

# تشغيل جميع الخدمات
docker-compose -f docker-compose.prod.yml up -d

# المشروع يعمل الآن على:
# - Frontend: http://localhost
# - Backend: http://localhost:8000
# - Database: localhost:5432
```

### إيقاف الخدمات

```bash
docker-compose -f docker-compose.prod.yml down
```

---

## ☁️ النشر على Production

### الخيارات المتاحة:

1. **Render.com** (موصى به)
   - نشر مجاني للبداية
   - دعم PostgreSQL
   - SSL تلقائي
   - [دليل النشر على Render](DEPLOYMENT_INSTRUCTIONS.md#option-1-deploy-backend-على-render)

2. **Railway.app**
   - واجهة سهلة
   - دعم Docker
   - قاعدة بيانات مُدارة
   - [دليل النشر على Railway](DEPLOYMENT_INSTRUCTIONS.md#option-2-deploy-backend-على-railway)

3. **Azure App Service**
   - للمشاريع الكبيرة
   - أداء عالي
   - [دليل النشر على Azure](DEPLOYMENT_INSTRUCTIONS.md#option-3-deploy-backend-على-azure)

---

## 🧪 الاختبار

### Backend Tests
```bash
cd backend
uv run pytest
```

### Frontend Tests
```bash
cd Flutter
flutter test
```

### End-to-End Test
```bash
# 1. تشغيل Backend
cd backend && uv run fastapi dev app/main.py

# 2. تشغيل Frontend
cd Flutter && flutter run -d chrome

# 3. اختبار التدفق الكامل
# Login → Dashboard → Assessment → Results
```

---

## 📊 التقنيات المستخدمة

### Backend
- **FastAPI**: إطار عمل حديث وسريع
- **OpenAI Whisper**: تحويل الصوت إلى نص
- **TextDistance**: حساب التشابه النصي
- **SQLModel**: ORM للتعامل مع قاعدة البيانات
- **Pydantic**: التحقق من البيانات
- **UV**: إدارة المكتبات السريعة

### Frontend
- **Flutter**: إطار عمل متعدد المنصات
- **HTTP Package**: للاتصال بالـ API
- **Google Fonts**: خط Cairo
- **Material Design 3**: تصميم حديث

### DevOps
- **Docker**: containerization
- **GitHub Actions**: CI/CD
- **PostgreSQL**: قاعدة بيانات
- **Nginx**: خادم ويب

---

## 🤝 المساهمة

نرحب بجميع المساهمات! 

### كيفية المساهمة:
1. Fork المشروع
2. أنشئ branch جديد (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push للـ branch (`git push origin feature/AmazingFeature`)
5. افتح Pull Request

---

## 📝 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

---

## 👨‍💻 المطورون

- **المطور الرئيسي**: [kk121288](https://github.com/kk121288)
- **المساهمون**: [قائمة المساهمين](https://github.com/kk121288/BTEC-backend/graphs/contributors)

---

## 📞 الدعم

- **Issues**: [GitHub Issues](https://github.com/kk121288/BTEC-backend/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kk121288/BTEC-backend/discussions)
- **Email**: support@btec-platform.com

---

## 🗺️ خارطة الطريق

- [x] ✅ بناء Backend API
- [x] ✅ تكامل Whisper
- [x] ✅ تقييم نصي ذكي
- [x] ✅ واجهة Flutter
- [x] ✅ لوحة التحكم
- [ ] 🔄 نظام الإشعارات
- [ ] 🔄 تقارير متقدمة
- [ ] 🔄 دعم متعدد اللغات
- [ ] 🔄 تطبيق موبايل كامل

---

<div align="center">

**صُنع بـ ❤️ للتعليم**

⭐ إذا أعجبك المشروع، لا تنسى النجمة! ⭐

</div>
