#!/usr/bin/env python
"""
ملف تشغيل خادم Django - عدستي
تشغيل الخادم مع إعدادات محسنة للتطوير والإنتاج
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# إضافة مجلد المشروع إلى Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# إعداد متغير البيئة لـ Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visionlens_store.settings')

def print_banner():
    """طباعة شعار المشروع"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                    👁️  عدستي - VisionLens                    ║
    ║                   متجر العدسات اللاصقة                      ║
    ║                                                              ║
    ║                  🚀 خادم Django قيد التشغيل                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """التحقق من المتطلبات"""
    try:
        import django
        print(f"✅ Django {django.get_version()} - مثبت")
    except ImportError:
        print("❌ Django غير مثبت!")
        print("قم بتثبيته: pip install Django==4.2.7")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow - مثبت")
    except ImportError:
        print("⚠️  Pillow غير مثبت (مطلوب للصور)")
        print("قم بتثبيته: pip install Pillow==10.0.1")
    
    return True

def run_migrations():
    """تشغيل الهجرات"""
    print("\n🔄 تشغيل هجرات قاعدة البيانات...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ تم تشغيل الهجرات بنجاح")
    except subprocess.CalledProcessError:
        print("❌ فشل في تشغيل الهجرات")
        return False
    return True

def collect_static():
    """جمع الملفات الثابتة"""
    print("\n📁 جمع الملفات الثابتة...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("✅ تم جمع الملفات الثابتة بنجاح")
    except subprocess.CalledProcessError:
        print("❌ فشل في جمع الملفات الثابتة")
        return False
    return True

def create_superuser():
    """إنشاء مستخدم مدير إذا لم يكن موجود"""
    print("\n👤 التحقق من وجود مستخدم مدير...")
    try:
        from django.contrib.auth import get_user_model
        import django
        django.setup()
        
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            print("📝 إنشاء مستخدم مدير افتراضي...")
            User.objects.create_superuser(
                username='admin',
                email='admin@visionlens.com',
                password='admin123'
            )
            print("✅ تم إنشاء مستخدم مدير:")
            print("   اسم المستخدم: admin")
            print("   كلمة المرور: admin123")
        else:
            print("✅ مستخدم مدير موجود بالفعل")
    except Exception as e:
        print(f"⚠️  تعذر إنشاء مستخدم مدير: {e}")

def get_local_ip():
    """الحصول على عنوان IP المحلي"""
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return "127.0.0.1"

def run_server(host='127.0.0.1', port='8000', debug=True):
    """تشغيل خادم Django"""
    print(f"\n🌐 تشغيل خادم Django...")
    print(f"📍 العنوان المحلي: http://{host}:{port}/")
    
    # الحصول على IP المحلي للوصول من أجهزة أخرى
    local_ip = get_local_ip()
    if local_ip != '127.0.0.1':
        print(f"🌍 الوصول من الشبكة: http://{local_ip}:{port}/")
    
    print(f"🔧 لوحة الإدارة: http://{host}:{port}/admin/")
    print(f"📊 لوحة التحكم: http://{host}:{port}/dashboard/")
    print("\n⏹️  اضغط Ctrl+C لإيقاف الخادم")
    print("=" * 60)
    
    try:
        if debug:
            # تشغيل في وضع التطوير
            subprocess.run([
                sys.executable, 'manage.py', 'runserver', 
                f'{host}:{port}', '--settings=visionlens_store.settings'
            ])
        else:
            # تشغيل في وضع الإنتاج مع gunicorn
            subprocess.run([
                'gunicorn', 'visionlens_store.wsgi:application',
                '--bind', f'{host}:{port}',
                '--workers', '3',
                '--timeout', '120'
            ])
    except KeyboardInterrupt:
        print("\n\n🛑 تم إيقاف الخادم")
    except FileNotFoundError:
        print("❌ gunicorn غير مثبت للوضع الإنتاجي")
        print("قم بتثبيته: pip install gunicorn")

def main():
    """الدالة الرئيسية"""
    print_banner()
    
    # التحقق من المتطلبات
    if not check_requirements():
        return
    
    # تشغيل الإعدادات الأولية
    if not run_migrations():
        return
    
    # جمع الملفات الثابتة
    collect_static()
    
    # إنشاء مستخدم مدير
    create_superuser()
    
    # خيارات التشغيل
    print("\n" + "=" * 60)
    print("🎯 خيارات التشغيل:")
    print("1. تطوير (Development) - المنفذ 8000")
    print("2. تطوير مع إمكانية الوصول من الشبكة - المنفذ 8000")
    print("3. إنتاج (Production) مع Gunicorn - المنفذ 8000")
    print("4. مخصص - اختر المنفذ والعنوان")
    print("5. خروج")
    
    try:
        choice = input("\nاختر رقم الخيار (1-5): ").strip()
        
        if choice == '1':
            run_server('127.0.0.1', '8000', debug=True)
        elif choice == '2':
            run_server('0.0.0.0', '8000', debug=True)
        elif choice == '3':
            run_server('0.0.0.0', '8000', debug=False)
        elif choice == '4':
            host = input("أدخل العنوان (افتراضي 127.0.0.1): ").strip() or '127.0.0.1'
            port = input("أدخل المنفذ (افتراضي 8000): ").strip() or '8000'
            mode = input("وضع التطوير؟ (y/n): ").strip().lower()
            debug = mode in ['y', 'yes', 'نعم']
            run_server(host, port, debug)
        elif choice == '5':
            print("👋 وداع<|im_start|>!")
            return
        else:
            print("❌ خيار غير صحيح")
            
    except KeyboardInterrupt:
        print("\n👋 تم الإلغاء")

if __name__ == '__main__':
    main()
