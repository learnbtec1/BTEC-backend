
# push-to-github.ps1
param(
    [string]$CommitMessage = "Update project",
    [string]$Branch = "main",
    [string]$Remote = "origin"
)

# التحقق من وجود Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git غير مثبت على هذا الجهاز." -ForegroundColor Red
    exit
}

Write-Host "🔍 التحقق من حالة المستودع..." -ForegroundColor Cyan
git status

Write-Host "➕ إضافة جميع الملفات..." -ForegroundColor Yellow
git add .

Write-Host "📝 إنشاء Commit بالرسالة: $CommitMessage" -ForegroundColor Yellow
git commit -m "$CommitMessage"

Write-Host "⬆ رفع التغييرات إلى $Remote/$Branch ..." -ForegroundColor Yellow
git push $Remote $Branch

Write-Host "✅ تم رفع التغييرات بنجاح إلى الفرع $Branch على المستودع $Remote." -ForegroundColor Green
