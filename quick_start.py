#!/usr/bin/env python
"""
تشغيل سريع لخادم عدستي - VisionLens
Quick start script for VisionLens Django server
"""

import os
import sys
import subprocess
import webbrowser
import time

def print_banner():
    """طباعة شعار المشروع"""
    print("\n" + "="*60)
    print("                  👁️  عدستي - VisionLens")
    print("                 متجر العدسات اللاصقة")
    print("="*60)

def install_requirements():
    """تثبيت المتطلبات الأساسية"""
    print("📦 تثبيت المكتبات الأساسية...")
    requirements = [
        'Django==4.2.7',
        'Pillow==10.0.1', 
        'whitenoise==6.6.0'
    ]
    
    try:
        for req in requirements:
            subprocess.run([sys.executable, '-m', 'pip', 'install', req], 
                         check=True, capture_output=True, text=True)
        print("✅ تم تثبيت جميع المكتبات بنجاح")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  تعذر تثبيت بعض المكتبات: {e}")
        return False

def setup_database():
    """إعداد قاعدة البيانات"""
    print("📊 إعداد قاعدة البيانات...")
    try:
        # تشغيل الهجرات
        subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                      check=True, capture_output=True)
        print("✅ تم إعداد قاعدة البيانات")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  تعذر إعداد قاعدة البيانات")
        return False

def collect_static():
    """جمع الملفات الثابتة"""
    print("📁 جمع الملفات الثابتة...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                      check=True, capture_output=True)
        print("✅ تم جمع الملفات الثابتة")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  تعذر جمع الملفات الثابتة")
        return False

def create_admin_user():
    """إنشاء مستخدم مدير"""
    print("👤 إعداد مستخدم الإدارة...")
    
    # إنشاء ملف Python مؤقت
    script_content = '''
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visionlens_store.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@visionlens.com", "admin123")
    print("✅ تم إنشاء مستخدم مدير جديد")
    print("   اسم المستخدم: admin")
    print("   كلمة المرور: admin123")
else:
    print("✅ مستخدم مدير موجود بالفعل")
'''
    
    try:
        # كتابة الملف المؤقت
        with open('temp_create_user.py', 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # تشغيل الملف
        result = subprocess.run([sys.executable, 'temp_create_user.py'], 
                              capture_output=True, text=True)
        
        # حذف الملف المؤقت
        os.remove('temp_create_user.py')
        
        if result.returncode == 0:
            print("✅ تم إعداد مستخدم الإدارة")
            return True
        else:
            print("⚠️  تعذر إعداد مستخدم الإدارة")
            return False
            
    except Exception as e:
        print(f"⚠️  خطأ في إعداد مستخدم الإدارة: {e}")
        return False

def start_server():
    """تشغيل الخادم"""
    print("\n" + "="*60)
    print("🌐 تشغيل خادم Django...")
    print("📍 الموقع الرئيسي: http://127.0.0.1:8000/")
    print("🔧 لوحة الإدارة: http://127.0.0.1:8000/admin/")
    print("📊 لوحة التحكم: http://127.0.0.1:8000/dashboard/")
    print("\n🔐 معلومات تسجيل الدخول:")
    print("   👤 اسم المستخدم: admin")
    print("   🔑 كلمة المرور: admin123")
    print("\n⏹️  اضغط Ctrl+C لإيقاف الخادم")
    print("="*60)
    
    # فتح المتصفح تلقائ<|im_start|>
    try:
        time.sleep(2)  # انتظار قصير
        webbrowser.open('http://127.0.0.1:8000/')
        print("🌐 تم فتح المتصفح تلقائ<|im_start|>")
    except:
        print("⚠️  تعذر فتح المتصفح تلقائ<|im_start|>")
    
    try:
        # تشغيل الخادم
        subprocess.run([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])
    except KeyboardInterrupt:
        print("\n\n🛑 تم إيقاف الخادم بنجاح")
        print("👋 شكراً لاستخدام عدستي!")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل الخادم: {e}")

def main():
    """الدالة الرئيسية"""
    # إعداد متغير البيئة
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visionlens_store.settings')
    
    # طباعة الشعار
    print_banner()
    
    # تشغيل الإعدادات
    steps = [
        ("تثبيت المكتبات", install_requirements),
        ("إعداد قاعدة البيانات", setup_database),
        ("جمع الملفات الثابتة", collect_static),
        ("إعداد مستخدم الإدارة", create_admin_user)
    ]
    
    print("\n🚀 بدء إعداد المشروع...")
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"❌ فشل في: {step_name}")
            print("💡 جرب تشغيل الأمر مرة أخرى")
            return
    
    print("\n🎉 تم إعداد المشروع بنجاح!")
    
    # تشغيل الخادم
    start_server()

if __name__ == '__main__':
    main()
