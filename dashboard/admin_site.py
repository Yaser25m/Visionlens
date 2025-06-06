from django.contrib.admin import AdminSite
from django.urls import path
from .views import admin_index_view


class CustomAdminSite(AdminSite):
    """موقع إدارة مخصص مع تصميم محسن"""
    
    site_header = 'لوحة إدارة عدستي'
    site_title = 'إدارة عدستي'
    index_title = 'مرحباً بك في لوحة إدارة عدستي'
    
    def index(self, request, extra_context=None):
        """صفحة الفهرس المخصصة"""
        return admin_index_view(request, extra_context)
    
    def get_urls(self):
        """URLs مخصصة للموقع"""
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', admin_index_view, name='dashboard'),
        ]
        return custom_urls + urls


# إنشاء موقع إدارة مخصص
custom_admin_site = CustomAdminSite(name='custom_admin')
