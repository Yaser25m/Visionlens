#!/usr/bin/env python
"""
ملف تشغيل سريع لخادم Django - عدستي
"""

import os
import sys
import subprocess

def main():
    """تشغيل سريع للخادم"""
    print("🚀 تشغيل خادم عدستي...")
    
    # إعداد Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visionlens_store.settings')
    
    try:
        # تشغيل الهجرات
        print("📊 تحديث قاعدة البيانات...")
        subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], check=True)
        
        # جمع الملفات الثابتة
        print("📁 جمع الملفات الثابتة...")
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        
        # تشغيل الخادم
        print("🌐 تشغيل الخادم على http://127.0.0.1:8000/")
        print("🔧 لوحة الإدارة: http://127.0.0.1:8000/admin/")
        print("📊 لوحة التحكم: http://127.0.0.1:8000/dashboard/")
        print("⏹️  اضغط Ctrl+C لإيقاف الخادم\n")
        
        subprocess.run([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])
        
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف الخادم")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == '__main__':
    main()
