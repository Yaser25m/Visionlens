# ملف تشغيل PowerShell لخادم Django - عدستي

# تعيين ترميز UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# ألوان
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$Cyan = "Cyan"
$Magenta = "Magenta"

# شعار المشروع
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║                    👁️  عدستي - VisionLens                    ║" -ForegroundColor Cyan
Write-Host "║                   متجر العدسات اللاصقة                      ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║                  🚀 تشغيل خادم Django                        ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# التحقق من وجود Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python مثبت: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python غير مثبت" -ForegroundColor Red
    exit 1
}

# تثبيت المتطلبات
Write-Host "📦 تثبيت المتطلبات..." -ForegroundColor Yellow
try {
    pip install -r requirements_minimal.txt --quiet
    Write-Host "✅ تم تثبيت المتطلبات" -ForegroundColor Green
} catch {
    Write-Host "⚠️  تعذر تثبيت بعض المتطلبات" -ForegroundColor Yellow
}

# تشغيل الهجرات
Write-Host "📊 تحديث قاعدة البيانات..." -ForegroundColor Blue
python manage.py makemigrations
python manage.py migrate

# جمع الملفات الثابتة
Write-Host "📁 جمع الملفات الثابتة..." -ForegroundColor Magenta
python manage.py collectstatic --noinput

# إنشاء مستخدم مدير
Write-Host "Setup admin user..." -ForegroundColor Green
$createSuperuser = @'
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visionlens_store.settings")
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@visionlens.com", "admin123")
    print("Admin user created: admin / admin123")
else:
    print("Admin user already exists")
'@

$createSuperuser | python

Write-Host ""
Write-Host "Starting Django server..." -ForegroundColor Green
Write-Host "Website: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Admin Panel: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host "Dashboard: http://127.0.0.1:8000/dashboard/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════"
Write-Host ""

# تشغيل الخادم
python manage.py runserver 127.0.0.1:8000
