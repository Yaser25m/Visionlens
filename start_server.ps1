# VisionLens Django Server Startup Script
# Simple PowerShell script to start the Django development server

# Set UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Colors
$Green = "Green"
$Blue = "Blue"
$Yellow = "Yellow"
$Cyan = "Cyan"

# Banner
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    VisionLens - Django Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements_minimal.txt --quiet

# Run migrations
Write-Host "Running migrations..." -ForegroundColor Blue
python manage.py makemigrations
python manage.py migrate

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Blue
python manage.py collectstatic --noinput

# Create superuser script
Write-Host "Setting up admin user..." -ForegroundColor Green
$pythonScript = @"
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visionlens_store.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@visionlens.com', 'admin123')
    print('Admin user created: admin / admin123')
else:
    print('Admin user already exists')
"@

# Save Python script to temp file and execute
$tempFile = [System.IO.Path]::GetTempFileName() + ".py"
$pythonScript | Out-File -FilePath $tempFile -Encoding UTF8
python $tempFile
Remove-Item $tempFile

Write-Host ""
Write-Host "Starting Django server..." -ForegroundColor Green
Write-Host "Website: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Admin: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host "Dashboard: http://127.0.0.1:8000/dashboard/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Login: admin / admin123" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start server
python manage.py runserver 127.0.0.1:8000
