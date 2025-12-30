# 🚀 BTEC Smart Platform - دليل النشر الكامل

## 📋 المتطلبات الأساسية

### Backend:
- Python 3.11+
- PostgreSQL 14+
- UV Package Manager

### Frontend:
- Flutter 3.0+
- Dart SDK
- Android Studio / Xcode (للموبايل)

---

## 🔧 الإعداد المحلي (Local Development)

### 1. Backend Setup

```bash
# انتقل إلى مجلد Backend
cd backend

# تثبيت UV
pip install uv

# مزامنة المكتبات
uv sync

# إنشاء ملف .env
cp ../.env.example .env

# تعديل متغيرات البيئة
nano .env

# تشغيل Backend
uv run fastapi dev app/main.py
```

Backend سيعمل على: `http://localhost:8000`

### 2. Frontend Setup

```bash
# انتقل إلى مجلد Flutter
cd Flutter

# تثبيت المكتبات
flutter pub get

# تشغيل التطبيق
flutter run -d chrome  # للويب
flutter run            # للموبايل
```

---

## 🌐 النشر على Production

### Option 1: Deploy Backend على Render

1. اذهب إلى [render.com](https://render.com)
2. أنشئ حساب جديد
3. اضغط "New +" → "Web Service"
4. اربط GitHub Repository
5. املأ البيانات:
   - **Name**: btec-backend
   - **Region**: Frankfurt (EU Central)
   - **Branch**: main
   - **Root Directory**: backend
   - **Build Command**: `pip install uv && uv sync`
   - **Start Command**: `uv run fastapi run app/main.py --host 0.0.0.0 --port $PORT`
6. أضف Environment Variables من ملف `.env`
7. اضغط "Create Web Service"

### Option 2: Deploy Backend على Railway

1. اذهب إلى [railway.app](https://railway.app)
2. اضغط "New Project" → "Deploy from GitHub"
3. اختر Repository
4. أضف PostgreSQL Database
5. أضف Environment Variables
6. Deploy!

### Option 3: Deploy Backend على Azure

```bash
# تثبيت Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# تسجيل الدخول
az login

# إنشاء Resource Group
az group create --name btec-rg --location westeurope

# إنشاء App Service
az webapp up --name btec-backend --resource-group btec-rg --runtime "PYTHON:3.11"
```

---

## 📱 بناء Flutter للإنتاج

### بناء Web:

```bash
cd Flutter
flutter build web --release

# الملفات في: build/web/
```

### بناء Android:

```bash
flutter build apk --release
# الملف في: build/app/outputs/flutter-apk/app-release.apk
```

### بناء iOS:

```bash
flutter build ios --release
```

---

## 🔒 إعداد Domain + SSL

### استخدام Cloudflare (مجاني):

1. اشترِ Domain من Namecheap / GoDaddy
2. أضف Domain إلى Cloudflare
3. غيّر Nameservers في الموقع الأصلي
4. في Cloudflare:
   - SSL/TLS → Full
   - DNS → أضف A Record يشير إلى IP الخادم
5. SSL سيُفعَّل تلقائياً

---

## 🔄 إعداد CI/CD (GitHub Actions)

الملف موجود في: `.github/workflows/full-stack-auto.yml`

### تفعيل Workflow:

1. اذهب إلى Settings → Secrets → Actions
2. أضف:
   - `PROD_HOST`: IP أو Domain الخادم
   - `PROD_USER`: اسم المستخدم SSH
   - `PROD_SSH_KEY`: المفتاح الخاص SSH

### Workflow سيعمل تلقائياً عند:
- Push على branch `main`
- أو يدوياً من تبويب Actions

---

## ✅ اختبار End-to-End

### 1. اختبار Backend:

```bash
curl http://localhost:8000/api/v1/btec/evaluate/text \
  -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "student_answer=Hello&model_answer=Hello World"
```

### 2. اختبار Frontend:

1. افتح التطبيق
2. سجل دخول
3. اذهب إلى "التقييم"
4. أدخل نص للتقييم
5. تأكد من ظهور النتائج

---

## 📊 Monitoring

### Backend Health Check:

```bash
curl http://your-domain.com/api/v1/health
```

### Database Check:

```sql
SELECT * FROM pg_stat_activity;
```

---

## 🐛 Troubleshooting

### مشكلة: Backend لا يعمل

```bash
# تحقق من Logs
uv run python -c "from app.main import app; print('OK')"

# تحقق من Database
psql $DATABASE_URL
```

### مشكلة: Flutter build فشل

```bash
flutter clean
flutter pub get
flutter build web --verbose
```

---

## 📞 الدعم

للمساعدة أو الإبلاغ عن مشاكل:
- فتح Issue على GitHub
- التواصل عبر البريد الإلكتروني

---

**✨ الآن المشروع جاهز للإطلاق!**
