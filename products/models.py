from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    """فئات العدسات"""
    name = models.CharField(max_length=100, verbose_name="اسم الفئة")
    name_en = models.CharField(max_length=100, verbose_name="اسم الفئة بالإنجليزية")
    description = models.TextField(blank=True, verbose_name="الوصف")
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name="صورة الفئة")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "فئة"
        verbose_name_plural = "الفئات"
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    """العلامات التجارية"""
    name = models.CharField(max_length=100, verbose_name="اسم العلامة التجارية")
    logo = models.ImageField(upload_to='brands/', blank=True, verbose_name="شعار العلامة التجارية")
    description = models.TextField(blank=True, verbose_name="الوصف")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "علامة تجارية"
        verbose_name_plural = "العلامات التجارية"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """منتجات العدسات"""
    LENS_TYPE_CHOICES = [
        ('daily', 'يومية'),
        ('weekly', 'أسبوعية'),
        ('monthly', 'شهرية'),
        ('yearly', 'سنوية'),
    ]

    LENS_USAGE_CHOICES = [
        ('medical', 'طبية'),
        ('cosmetic', 'تجميلية'),
        ('both', 'طبية وتجميلية'),
    ]

    name = models.CharField(max_length=200, verbose_name="اسم المنتج")
    name_en = models.CharField(max_length=200, verbose_name="اسم المنتج بالإنجليزية")
    description = models.TextField(verbose_name="الوصف")
    description_en = models.TextField(verbose_name="الوصف بالإنجليزية")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="الفئة")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="العلامة التجارية")

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="سعر الخصم")

    lens_type = models.CharField(max_length=20, choices=LENS_TYPE_CHOICES, verbose_name="نوع العدسة")
    lens_usage = models.CharField(max_length=20, choices=LENS_USAGE_CHOICES, verbose_name="استخدام العدسة")

    color = models.CharField(max_length=50, verbose_name="اللون")
    power = models.CharField(max_length=20, blank=True, verbose_name="القوة")
    diameter = models.CharField(max_length=20, blank=True, verbose_name="القطر")
    base_curve = models.CharField(max_length=20, blank=True, verbose_name="انحناء القاعدة")

    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="الكمية المتوفرة")
    min_stock_level = models.PositiveIntegerField(default=10, verbose_name="الحد الأدنى للمخزون")

    # Main image field
    main_image = models.ImageField(upload_to='products/main/', blank=True, null=True, verbose_name="الصورة الرئيسية")

    is_active = models.BooleanField(default=True, verbose_name="نشط")
    is_featured = models.BooleanField(default=False, verbose_name="مميز")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    @property
    def get_price(self):
        """إرجاع السعر النهائي (مع الخصم إن وجد)"""
        if self.discount_price:
            return self.discount_price
        return self.price

    @property
    def discount_percentage(self):
        """حساب نسبة الخصم"""
        if self.discount_price and self.price > self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    @property
    def is_in_stock(self):
        """التحقق من توفر المنتج"""
        return self.stock_quantity > 0

    @property
    def is_low_stock(self):
        """التحقق من انخفاض المخزون"""
        return self.stock_quantity <= self.min_stock_level


class ProductImage(models.Model):
    """صور المنتجات"""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name="المنتج")
    image = models.ImageField(upload_to='products/', verbose_name="الصورة")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="النص البديل")
    is_primary = models.BooleanField(default=False, verbose_name="صورة رئيسية")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "صورة منتج"
        verbose_name_plural = "صور المنتجات"
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"صورة {self.product.name}"
