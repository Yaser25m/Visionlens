#!/usr/bin/env python
"""
🚀 عدستي - VisionLens Server
ملف تشغيل واحد للخادم - يعمل على جميع الأنظمة
"""

import os
import sys
import subprocess
import platform
import webbrowser
import time

def clear_screen():
    """مسح الشاشة"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_logo():
    """طباعة شعار المشروع"""
    clear_screen()
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    👁️  عدستي - VisionLens                    ║
║                   متجر العدسات اللاصقة                      ║
║                                                              ║
║                  🚀 خادم Django - تشغيل واحد                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

def run_command(command, description, show_output=False):
    """تشغيل أمر مع معالجة الأخطاء"""
    print(f"🔄 {description}...")
    try:
        if show_output:
            result = subprocess.run(command, check=True, shell=True)
        else:
            result = subprocess.run(command, check=True, shell=True, 
                                  capture_output=True, text=True)
        print(f"✅ {description} - تم بنجاح")
        return True
    except subprocess.CalledProcessError:
        print(f"⚠️  {description} - فشل (سيتم المتابعة)")
        return False
    except Exception as e:
        print(f"❌ {description} - خطأ: {e}")
        return False

def update_allowed_hosts():
    """تحديث ALLOWED_HOSTS بـ IP المحلي"""
    local_ip = get_local_ip()
    if local_ip:
        print(f"🔧 إضافة {local_ip} إلى ALLOWED_HOSTS...")
        try:
            # قراءة ملف settings.py
            with open('visionlens_store/settings.py', 'r', encoding='utf-8') as f:
                content = f.read()

            # إضافة IP إذا لم يكن موجود
            if local_ip not in content:
                # البحث عن ALLOWED_HOSTS وإضافة IP
                if "'*'," not in content:
                    content = content.replace(
                        "'0.0.0.0',",
                        f"'0.0.0.0',\n    '{local_ip}',  # IP المحلي التلقائي"
                    )

                    # كتابة الملف
                    with open('visionlens_store/settings.py', 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ تم إضافة {local_ip} إلى ALLOWED_HOSTS")
                else:
                    print("✅ ALLOWED_HOSTS يقبل جميع العناوين")
            else:
                print(f"✅ {local_ip} موجود بالفعل في ALLOWED_HOSTS")
        except Exception as e:
            print(f"⚠️  تعذر تحديث ALLOWED_HOSTS: {e}")

def setup_project():
    """إعداد المشروع كاملاً"""
    print("🔧 بدء إعداد المشروع...\n")

    # إعداد متغير البيئة
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visionlens_store.settings')

    # تحديث ALLOWED_HOSTS
    update_allowed_hosts()
    
    # تثبيت المكتبات الأساسية
    packages = ['Django==4.2.7', 'Pillow==10.0.1', 'whitenoise==6.6.0']
    for package in packages:
        run_command(f'pip install {package}', f'تثبيت {package.split("==")[0]}')
    
    # إعداد قاعدة البيانات
    run_command('python manage.py makemigrations', 'إنشاء الهجرات')
    run_command('python manage.py migrate', 'تطبيق الهجرات')
    
    # جمع الملفات الثابتة
    run_command('python manage.py collectstatic --noinput', 'جمع الملفات الثابتة')
    
    # إنشاء مستخدم مدير
    create_admin_user()
    
    print("\n🎉 تم إعداد المشروع بنجاح!")

def create_admin_user():
    """إنشاء مستخدم مدير"""
    print("👤 إعداد مستخدم الإدارة...")
    
    script = '''
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visionlens_store.settings")
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@visionlens.com", "admin123")
    print("تم إنشاء مستخدم مدير جديد")
else:
    print("مستخدم مدير موجود بالفعل")
'''
    
    try:
        with open('temp_admin.py', 'w', encoding='utf-8') as f:
            f.write(script)
        
        subprocess.run([sys.executable, 'temp_admin.py'], check=True)
        os.remove('temp_admin.py')
        print("✅ تم إعداد مستخدم الإدارة")
    except:
        print("⚠️  تعذر إعداد مستخدم الإدارة")

def get_local_ip():
    """الحصول على عنوان IP المحلي"""
    try:
        import socket
        # طريقة أفضل للحصول على IP المحلي
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        try:
            # طريقة بديلة
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except:
            return None

def check_network_connectivity():
    """فحص الاتصال بالشبكة"""
    import socket
    try:
        # فحص المنفذ 8000
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 8000))
        sock.close()
        return result == 0
    except:
        return False

def start_server(network_access=True):
    """تشغيل الخادم"""
    print("\n" + "="*60)
    print("🌐 تشغيل خادم Django...")

    # الحصول على IP المحلي
    local_ip = get_local_ip()

    print("\n📍 روابط الوصول:")
    print("   🏠 من هذا الجهاز: http://127.0.0.1:8000/")
    print("   🔧 لوحة الإدارة: http://127.0.0.1:8000/admin/")
    print("   📊 لوحة التحكم: http://127.0.0.1:8000/dashboard/")

    if network_access and local_ip and local_ip != '127.0.0.1':
        print(f"\n🌍 من أجهزة أخرى في نفس الشبكة:")
        print(f"   🏠 الصفحة الرئيسية: http://{local_ip}:8000/")
        print(f"   🔧 لوحة الإدارة: http://{local_ip}:8000/admin/")
        print(f"   📊 لوحة التحكم: http://{local_ip}:8000/dashboard/")
        print(f"\n💡 شارك هذا الرابط مع الأجهزة الأخرى: http://{local_ip}:8000/")
        print(f"\n📱 للموبايل/التابلت: افتح المتصفح واكتب: http://{local_ip}:8000/")
        print(f"🔥 تأكد من أن جدار الحماية (Firewall) لا يحجب المنفذ 8000")
    elif not network_access:
        print("\n🔒 الوصول محدود لهذا الجهاز فقط")
    else:
        print("\n⚠️  تعذر الحصول على عنوان IP المحلي")
    
    print("\n🔐 معلومات تسجيل الدخول:")
    print("   👤 اسم المستخدم: admin")
    print("   🔑 كلمة المرور: admin123")
    
    print("\n⏹️  اضغط Ctrl+C لإيقاف الخادم")
    print("="*60)
    
    # فتح المتصفح بعد 3 ثواني
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://127.0.0.1:8000/')
            print("\n🌐 تم فتح المتصفح تلقائياً")
        except:
            pass
    
    # تشغيل فتح المتصفح في الخلفية
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # تشغيل الخادم
        if network_access:
            # السماح بالوصول من الشبكة
            subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])
        else:
            # الوصول المحلي فقط
            subprocess.run([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])
    except KeyboardInterrupt:
        print("\n\n🛑 تم إيقاف الخادم")
        print("👋 شكراً لاستخدام عدستي!")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل الخادم: {e}")

def check_python():
    """التحقق من Python"""
    try:
        version = sys.version.split()[0]
        print(f"✅ Python {version} - جاهز")
        return True
    except:
        print("❌ Python غير متوفر")
        return False

def main():
    """الدالة الرئيسية"""
    print_logo()
    
    # التحقق من Python
    if not check_python():
        input("اضغط Enter للخروج...")
        return
    
    print("🚀 مرحباً بك في خادم عدستي!")
    print("\nاختر ما تريد فعله:")
    print("1️⃣  تشغيل سريع + شبكة (يمكن الوصول من أجهزة أخرى)")
    print("2️⃣  إعداد كامل + تشغيل + شبكة")
    print("3️⃣  تشغيل محلي فقط (هذا الجهاز فقط)")
    print("4️⃣  خروج")

    try:
        choice = input("\nاختر رقم (1-4) أو اضغط Enter للتشغيل مع الشبكة: ").strip()

        # إذا لم يختر شيء، استخدم الخيار الأول
        if not choice:
            choice = '1'
        
        if choice == '1':
            print("\n🚀 تشغيل سريع مع الشبكة...")
            update_allowed_hosts()  # تحديث ALLOWED_HOSTS
            start_server(network_access=True)

        elif choice == '2':
            print("\n🔧 إعداد كامل مع الشبكة...")
            setup_project()
            input("\nاضغط Enter لبدء تشغيل الخادم...")
            start_server(network_access=True)

        elif choice == '3':
            print("\n🔒 تشغيل محلي فقط...")
            start_server(network_access=False)

        elif choice == '4':
            print("\n👋 وداعاً!")
            return
            
        else:
            print("\n❌ خيار غير صحيح")
            input("اضغط Enter للمحاولة مرة أخرى...")
            main()
            
    except KeyboardInterrupt:
        print("\n\n👋 تم الإلغاء")
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        input("اضغط Enter للخروج...")

if __name__ == '__main__':
    main()
