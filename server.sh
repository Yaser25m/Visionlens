#!/bin/bash

# تعيين ترميز UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# ألوان للنص
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# شعار المشروع
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║                    👁️  عدستي - VisionLens                    ║"
echo "║                   متجر العدسات اللاصقة                      ║"
echo "║                                                              ║"
echo "║                  🚀 تشغيل خادم Django                        ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 غير مثبت${NC}"
    exit 1
fi

# التحقق من وجود pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 غير مثبت${NC}"
    exit 1
fi

# تثبيت المتطلبات إذا لم تكن مثبتة
echo -e "${YELLOW}📦 التحقق من المتطلبات...${NC}"
pip3 install -r requirements_minimal.txt --quiet

# تشغيل الهجرات
echo -e "${BLUE}📊 تحديث قاعدة البيانات...${NC}"
python3 manage.py makemigrations
python3 manage.py migrate

# جمع الملفات الثابتة
echo -e "${PURPLE}📁 جمع الملفات الثابتة...${NC}"
python3 manage.py collectstatic --noinput

# إنشاء مستخدم مدير إذا لم يكن موجود
echo -e "${GREEN}👤 التحقق من مستخدم الإدارة...${NC}"
python3 -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visionlens_store.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@visionlens.com', 'admin123')
    print('✅ تم إنشاء مستخدم مدير: admin / admin123')
else:
    print('✅ مستخدم مدير موجود بالفعل')
"

echo ""
echo -e "${GREEN}🌐 تشغيل الخادم...${NC}"
echo -e "${CYAN}📍 الموقع: http://127.0.0.1:8000/${NC}"
echo -e "${CYAN}🔧 لوحة الإدارة: http://127.0.0.1:8000/admin/${NC}"
echo -e "${CYAN}📊 لوحة التحكم: http://127.0.0.1:8000/dashboard/${NC}"
echo ""
echo -e "${YELLOW}⏹️  اضغط Ctrl+C لإيقاف الخادم${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""

# تشغيل الخادم
python3 manage.py runserver 127.0.0.1:8000
