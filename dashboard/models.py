from django.db import models
from django.contrib.auth.models import User


class DashboardSettings(models.Model):
    """إعدادات لوحة التحكم"""
    site_name = models.CharField(max_length=100, default='عدستي', verbose_name='اسم الموقع')
    site_description = models.TextField(default='متجر العدسات اللاصقة الأول في العراق', verbose_name='وصف الموقع')
    contact_email = models.EmailField(default='info@visionlens.com', verbose_name='البريد الإلكتروني')
    contact_phone = models.CharField(max_length=20, default='+964 770 123 4567', verbose_name='رقم الهاتف')
    address = models.TextField(default='بغداد، العراق', verbose_name='العنوان')

    # إعدادات الشحن
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=50000, verbose_name='حد الشحن المجاني')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=5000, verbose_name='تكلفة الشحن')

    # إعدادات التصميم
    primary_color = models.CharField(max_length=7, default='#007bff', verbose_name='اللون الأساسي')
    secondary_color = models.CharField(max_length=7, default='#6c757d', verbose_name='اللون الثانوي')

    # إعدادات SEO
    meta_keywords = models.TextField(blank=True, verbose_name='الكلمات المفتاحية')
    meta_description = models.TextField(blank=True, verbose_name='وصف الميتا')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'إعدادات لوحة التحكم'
        verbose_name_plural = 'إعدادات لوحة التحكم'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # التأكد من وجود سجل واحد فقط
        if not self.pk and DashboardSettings.objects.exists():
            raise ValueError('يمكن إنشاء سجل واحد فقط من إعدادات لوحة التحكم')
        super().save(*args, **kwargs)


class AdminActivity(models.Model):
    """سجل أنشطة المديرين"""
    ACTION_CHOICES = [
        ('create', 'إنشاء'),
        ('update', 'تحديث'),
        ('delete', 'حذف'),
        ('login', 'تسجيل دخول'),
        ('logout', 'تسجيل خروج'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='المستخدم')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='النشاط')
    model_name = models.CharField(max_length=100, blank=True, verbose_name='اسم النموذج')
    object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name='معرف الكائن')
    description = models.TextField(blank=True, verbose_name='الوصف')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='عنوان IP')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='الوقت')

    class Meta:
        verbose_name = 'نشاط إداري'
        verbose_name_plural = 'الأنشطة الإدارية'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username} - {self.get_action_display()} - {self.timestamp}'
