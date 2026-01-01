param(
    [string]$RepoPath = "D:\BTEC-backend",   # عدّل المسار لمشروعك الحقيقي
    [string]$Branch = "main"
)

# تحقق أن المجلد موجود
if (-not (Test-Path $RepoPath)) {
    Write-Host "`n[خطأ]: المجلد $RepoPath غير موجود." -ForegroundColor Red
    exit
}

# انتقل إلى مجلد المشروع
Set-Location $RepoPath

Write-Host "`n--- مزامنة التعديلات مع GitHub ---" -ForegroundColor Cyan

try {
    # تحقق من وجود تعديلات غير محفوظة
    $status = git status --porcelain
    if ($status) {
        Write-Host "`n[تنبيه]: لديك تعديلات غير محفوظة." -ForegroundColor Yellow
        Write-Host "اختر أحد الخيارات التالية:" -ForegroundColor Cyan
        Write-Host "1. حفظ التعديلات (commit)" -ForegroundColor White
        Write-Host "2. حفظ مؤقت (stash)" -ForegroundColor White
        Write-Host "3. تجاهل التعديلات (reset --hard)" -ForegroundColor White

        $choice = Read-Host "أدخل رقم الخيار (افتراضي = 1)"
        if ([string]::IsNullOrWhiteSpace($choice)) { $choice = "1" }

        switch ($choice) {
            "1" {
                git add .
                $commitMessage = "Auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
                git commit -m $commitMessage
                Write-Host "`n[✔] تم حفظ التعديلات." -ForegroundColor Green
            }
            "2" {
                git stash
                Write-Host "`n[✔] تم حفظ التعديلات مؤقتًا." -ForegroundColor Green
            }
            "3" {
                git reset --hard
                Write-Host "`n[✔] تم تجاهل التعديلات." -ForegroundColor Green
            }
            default {
                Write-Host "`n[خطأ]: خيار غير صحيح." -ForegroundColor Red
                exit
            }
        }
    }

    # 1. جلب آخر التحديثات من GitHub
    Write-Host "`n[جلب التحديثات من GitHub...]" -ForegroundColor Yellow
    git pull origin $Branch

    # 2. إضافة أي تعديلات جديدة بعد الدمج
    git add .
    $commitMessage = "Auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git commit -m $commitMessage

    # 3. إرسال التعديلات إلى GitHub
    Write-Host "`n[إرسال التعديلات إلى GitHub...]" -ForegroundColor Yellow
    git push origin $Branch

    Write-Host "`n✅ تمت المزامنة بنجاح!" -ForegroundColor Green
}
catch {
    Write-Host "`n[خطأ]: $_" -ForegroundColor Red
}