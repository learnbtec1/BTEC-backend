# إعداد المسارات المحددة لمشروعك
$rootPath = "D:\BTEC-backend"
$backendPath = "$rootPath\backend"
$frontendPath = "$rootPath\frontend"

Clear-Host
Write-Host "--- 🌌 جاري تشغيل بروتوكول BTEC NEXUS الشامل ---" -ForegroundColor Cyan
Write-Host "الوقت الحالي: $(Get-Date)" -ForegroundColor DarkGray

# 1. تنظيف المنافذ القديمة لضمان عدم حدوث تداخل
Write-Host "[1/3] جاري تنظيف المنافذ القديمة..." -ForegroundColor Yellow
Stop-Process -Name "node" -ErrorAction SilentlyContinue
Stop-Process -Name "python" -ErrorAction SilentlyContinue

# 2. تشغيل الـ Backend (FastAPI على منفذ 10000)
Write-Host "[2/3] جاري تشغيل نواة البيانات (Backend)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $backendPath; uvicorn app.main:app --host 0.0.0.0 --port 10000 --reload"

# 3. تشغيل الـ Frontend (Vite على منفذ 5175)
Write-Host "[3/3] جاري تشغيل واجهة المستخدم (Frontend)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $frontendPath; npm run dev"

# 4. المزامنة وفتح البوابة
Write-Host "--- 🌐 جاري المزامنة مع الشبكة... ---" -ForegroundColor Blue
Start-Sleep -Seconds 7

$url = "http://localhost:5175"
Write-Host "✨ تم التشغيل بنجاح! البوابة مفتوحة الآن في: $url" -ForegroundColor Green
Start-Process $url