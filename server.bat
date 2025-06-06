@echo off
chcp 65001 >nul
title عدستي - خادم Django

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║                    👁️  عدستي - VisionLens                    ║
echo ║                   متجر العدسات اللاصقة                      ║
echo ║                                                              ║
echo ║                  🚀 تشغيل خادم Django                        ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📊 تحديث قاعدة البيانات...
python manage.py makemigrations
python manage.py migrate

echo.
echo 📁 جمع الملفات الثابتة...
python manage.py collectstatic --noinput

echo.
echo 🌐 تشغيل الخادم...
echo 📍 الموقع: http://127.0.0.1:8000/
echo 🔧 لوحة الإدارة: http://127.0.0.1:8000/admin/
echo 📊 لوحة التحكم: http://127.0.0.1:8000/dashboard/
echo.
echo ⏹️  اضغط Ctrl+C لإيقاف الخادم
echo ════════════════════════════════════════════════════════════════
echo.

python manage.py runserver 127.0.0.1:8000

pause
