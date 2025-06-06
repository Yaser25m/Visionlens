from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """ملف المستخدم الشخصي"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    phone = models.CharField(max_length=20, blank=True, verbose_name="رقم الهاتف")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاريخ الميلاد")
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'ذكر'), ('female', 'أنثى')],
        blank=True,
        verbose_name="الجنس"
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name="الصورة الشخصية")

    # تفضيلات المستخدم
    preferred_language = models.CharField(
        max_length=5,
        choices=[('ar', 'العربية'), ('en', 'English')],
        default='ar',
        verbose_name="اللغة المفضلة"
    )
    newsletter_subscription = models.BooleanField(default=True, verbose_name="اشتراك النشرة الإخبارية")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "ملف شخصي"
        verbose_name_plural = "الملفات الشخصية"

    def __str__(self):
        return f"ملف {self.user.username}"


class Address(models.Model):
    """عناوين المستخدمين"""
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE, verbose_name="المستخدم")
    title = models.CharField(max_length=50, verbose_name="عنوان العنوان")  # مثل: المنزل، العمل
    full_name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    address_line_1 = models.CharField(max_length=200, verbose_name="العنوان الأول")
    address_line_2 = models.CharField(max_length=200, blank=True, verbose_name="العنوان الثاني")
    city = models.CharField(max_length=50, verbose_name="المدينة")
    state = models.CharField(max_length=50, verbose_name="المنطقة/الولاية")
    postal_code = models.CharField(max_length=10, blank=True, verbose_name="الرمز البريدي")
    country = models.CharField(max_length=50, default="السعودية", verbose_name="البلد")
    is_default = models.BooleanField(default=False, verbose_name="عنوان افتراضي")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "عنوان"
        verbose_name_plural = "العناوين"
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def save(self, *args, **kwargs):
        # إذا كان هذا العنوان افتراضي، اجعل باقي العناوين غير افتراضية
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """إنشاء ملف شخصي تلقائياً عند إنشاء مستخدم جديد"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """حفظ الملف الشخصي عند حفظ المستخدم"""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
