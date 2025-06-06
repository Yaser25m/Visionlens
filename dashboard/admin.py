from django.contrib import admin
from .models import DashboardSettings, AdminActivity


@admin.register(DashboardSettings)
class DashboardSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'free_shipping_threshold', 'updated_at']
    fieldsets = (
        ('معلومات الموقع', {
            'fields': ('site_name', 'site_description', 'contact_email', 'contact_phone', 'address')
        }),
        ('إعدادات الشحن', {
            'fields': ('free_shipping_threshold', 'shipping_cost')
        }),
        ('إعدادات التصميم', {
            'fields': ('primary_color', 'secondary_color')
        }),
        ('إعدادات SEO', {
            'fields': ('meta_keywords', 'meta_description')
        }),
    )

    def has_add_permission(self, request):
        # السماح بإنشاء سجل واحد فقط
        return not DashboardSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # منع حذف الإعدادات
        return False


@admin.register(AdminActivity)
class AdminActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'timestamp', 'ip_address']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'description']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'description', 'ip_address', 'timestamp']

    def has_add_permission(self, request):
        # منع إضافة أنشطة يدوياً
        return False

    def has_change_permission(self, request, obj=None):
        # منع تعديل الأنشطة
        return False
