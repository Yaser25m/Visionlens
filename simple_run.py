#!/usr/bin/env python
"""
ملف تشغيل مبسط لخادم Django - عدستي
"""

import os
import sys
import subprocess

def main():
    """تشغيل الخادم بأبسط طريقة"""
    
    print("=" * 50)
    print("🚀 عدستي - VisionLens")
    print("=" * 50)
    
    # إعداد Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visionlens_store.settings')
    
    # تثبيت المكتبات الأساسية
    print("📦 تثبيت المكتبات الأساسية...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 
            'Django==4.2.7', 'Pillow==10.0.1', 'whitenoise==6.6.0'
        ], check=True, capture_output=True)
        print("✅ تم تثبيت المكتبات")
    except:
        print("⚠️  تعذر تثبيت بعض المكتبات")
    
    # تشغيل الهجرات
    print("📊 إعداد قاعدة البيانات...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True, capture_output=True)
        print("✅ تم إعداد قاعدة البيانات")
    except:
        print("⚠️  تعذر إعداد قاعدة البيانات")
    
    # جمع الملفات الثابتة
    print("📁 جمع الملفات الثابتة...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                      check=True, capture_output=True)
        print("✅ تم جمع الملفات الثابتة")
    except:
        print("⚠️  تعذر جمع الملفات الثابتة")
    
    # إنشاء مستخدم مدير
    print("👤 إعداد مستخدم الإدارة...")
    try:
        # استخدام shell command مباشر
        create_user_cmd = '''
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@visionlens.com", "admin123")
    print("تم إنشاء مستخدم مدير: admin / admin123")
else:
    print("مستخدم مدير موجود بالفعل")
'''
        subprocess.run([sys.executable, 'manage.py', 'shell', '-c', create_user_cmd], 
                      check=True, capture_output=True)
        print("✅ تم إعداد مستخدم الإدارة")
    except:
        print("⚠️  تعذر إعداد مستخدم الإدارة")
    
    print("\n" + "=" * 50)
    print("🌐 تشغيل الخادم...")
    print("📍 الموقع: http://127.0.0.1:8000/")
    print("🔧 لوحة الإدارة: http://127.0.0.1:8000/admin/")
    print("📊 لوحة التحكم: http://127.0.0.1:8000/dashboard/")
    print("\n🔐 معلومات تسجيل الدخول:")
    print("   اسم المستخدم: admin")
    print("   كلمة المرور: admin123")
    print("\n⏹️  اضغط Ctrl+C لإيقاف الخادم")
    print("=" * 50)
    print()
    
    try:
        # تشغيل الخادم
        subprocess.run([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف الخادم")
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")

if __name__ == '__main__':
    main()
