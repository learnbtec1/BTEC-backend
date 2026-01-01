# نظام مفاتيح التفعيل الذكي (Activation Key System)

## نظرة عامة

نظام مفاتيح التفعيل هو ميزة أمنية متكاملة تمكّن من إدارة تفعيل حسابات الطلاب في منصة BTEC. يوفر النظام إمكانية توليد مفاتيح تفعيل مشفرة، توزيعها، تتبع استخدامها، وإدارتها بشكل آمن.

## الميزات الرئيسية

- ✅ **توليد مفاتيح آمنة**: استخدام JWT لتوليد مفاتيح مشفرة وموقعة
- ✅ **تخزين آمن**: حفظ بيانات المفاتيح في قاعدة البيانات مع تشفير
- ✅ **تتبع الاستخدام**: تسجيل عدد مرات الاستخدام، آخر استخدام، وعنوان IP
- ✅ **إدارة دورة الحياة**: تاريخ انتهاء صلاحية، حالة التفعيل، إمكانية الإلغاء
- ✅ **ربط بالطالب**: ربط كل مفتاح برقم الطالب والبريد الإلكتروني والتخصص والمستوى

## التثبيت والإعداد

### 1. متغيرات البيئة

أضف المتغير التالي إلى ملف `.env`:

```bash
# سر تشفير مفاتيح التفعيل (يجب تغييره في الإنتاج!)
ACTIVATION_SECRET=your-super-secret-key-here-min-32-chars
```

⚠️ **تحذير أمني**: تأكد من استخدام مفتاح عشوائي قوي في بيئة الإنتاج. يمكنك توليد مفتاح آمن باستخدام:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. تطبيق Migration لقاعدة البيانات

قم بتطبيق migration لإنشاء جدول `activationkey`:

```bash
cd backend
alembic upgrade head
```

### 3. التحقق من التثبيت

تحقق من أن API متاح على المسار:
- `POST /api/v1/activation/admin/generate` - توليد مفاتيح (للمشرفين)
- `POST /api/v1/activation/activate` - تفعيل المفاتيح (للطلاب)

## الاستخدام

### توليد مفتاح تفعيل (للمشرفين)

**Endpoint**: `POST /api/v1/activation/admin/generate`

**المتطلبات**: يجب أن يكون المستخدم مسجل دخول (يحتاج access token)

**Request Body**:
```json
{
  "student_id": "STU12345",
  "student_email": "student@example.com",
  "specialization": "Computer Science",
  "level": "Level 3",
  "validity_days": 120
}
```

**Response**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "jti": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "expires_at": "2026-05-01T12:00:00Z"
}
```

**مثال باستخدام curl**:
```bash
curl -X POST "http://localhost:8000/api/v1/activation/admin/generate" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU12345",
    "student_email": "student@example.com",
    "specialization": "Computer Science",
    "level": "Level 3",
    "validity_days": 120
  }'
```

### تفعيل الحساب (للطلاب)

**Endpoint**: `POST /api/v1/activation/activate`

**المتطلبات**: لا يحتاج تسجيل دخول (عام)

**Request Body**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response**:
```json
{
  "status": "activated",
  "jti": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "student_id": "STU12345"
}
```

**مثال باستخدام curl**:
```bash
curl -X POST "http://localhost:8000/api/v1/activation/activate" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

## بنية قاعدة البيانات

### جدول `activationkey`

| العمود | النوع | الوصف |
|--------|-------|--------|
| `id` | Integer | المعرّف الرئيسي |
| `jti` | String (Unique) | معرّف JWT الفريد |
| `student_id` | String | رقم الطالب |
| `student_email` | String | البريد الإلكتروني للطالب |
| `specialization` | String | التخصص |
| `level` | String | المستوى الدراسي |
| `issued_at` | DateTime | تاريخ الإصدار |
| `expires_at` | DateTime | تاريخ انتهاء الصلاحية |
| `is_active` | Boolean | حالة التفعيل |
| `is_revoked` | Boolean | هل تم الإلغاء |
| `used_count` | Integer | عدد مرات الاستخدام |
| `last_used_at` | DateTime | آخر استخدام |
| `last_used_ip` | String | آخر IP |
| `metadata` | JSON | بيانات إضافية |

## التطويرات المستقبلية

### مخطط (TODO)

- [ ] إضافة endpoint لإدارة المفاتيح (`/admin/activation/list`, `/admin/activation/revoke`)
- [ ] نظام إشعارات قرب انتهاء الصلاحية
- [ ] ربط المفاتيح بحسابات الطلاب الفعلية في النظام
- [ ] إضافة قيود على عدد الأجهزة (Device Fingerprinting)
- [ ] تصدير تقارير استخدام المفاتيح
- [ ] إرسال بريد إلكتروني تلقائي عند توليد المفتاح
- [ ] واجهة إدارة للمشرفين

## الأمان

### أفضل الممارسات

1. **حماية السر (SECRET_KEY)**: لا تشارك `ACTIVATION_SECRET` أبداً في الكود أو Git
2. **HTTPS فقط**: استخدم HTTPS في الإنتاج لحماية نقل المفاتيح
3. **صلاحيات المشرف**: تأكد من تفعيل فحص صلاحيات المشرف في `/admin/generate`
4. **تدوير المفاتيح**: قم بتحديث `ACTIVATION_SECRET` دورياً
5. **مراقبة الاستخدام**: راقب محاولات التفعيل المتكررة من نفس IP

### معالجة الأخطاء

| رمز الخطأ | الوصف | الحل |
|-----------|--------|------|
| 400 | مفتاح غير صالح أو منتهي | تحقق من صحة المفتاح أو اطلب مفتاح جديد |
| 403 | مفتاح ملغى أو موقوف | اتصل بالدعم للحصول على مفتاح جديد |
| 404 | مفتاح غير موجود | تحقق من JTI أو اطلب مفتاح جديد |

## الاختبارات

تشغيل اختبارات نظام التفعيل:

```bash
cd backend
pytest tests/api/routes/test_activation.py -v
```

الاختبارات المتاحة:
- ✅ توليد مفتاح تفعيل
- ✅ تفعيل بمفتاح صالح
- ✅ رفض مفتاح غير صالح
- ✅ رفض مفتاح منتهي الصلاحية
- ✅ تتبع استخدام المفتاح

## الدعم

للإبلاغ عن مشاكل أو طلب ميزات جديدة، يرجى فتح issue في مستودع GitHub.

## الترخيص

هذا النظام جزء من مشروع BTEC Backend ويخضع لنفس الترخيص.
