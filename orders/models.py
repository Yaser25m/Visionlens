from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal


class Cart(models.Model):
    """سلة التسوق"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "سلة تسوق"
        verbose_name_plural = "سلال التسوق"

    def __str__(self):
        return f"سلة {self.user.username}"

    @property
    def total_items(self):
        """إجمالي عدد العناصر"""
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        """إجمالي السعر"""
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """عناصر سلة التسوق"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name="السلة")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")
    quantity = models.PositiveIntegerField(default=1, verbose_name="الكمية")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "عنصر سلة"
        verbose_name_plural = "عناصر السلة"
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    @property
    def total_price(self):
        """إجمالي سعر العنصر"""
        return self.product.get_price * self.quantity


class Order(models.Model):
    """الطلبات"""
    STATUS_CHOICES = [
        ('pending', 'في الانتظار'),
        ('confirmed', 'مؤكد'),
        ('processing', 'قيد التحضير'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التوصيل'),
        ('cancelled', 'ملغي'),
        ('returned', 'مرتجع'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'في الانتظار'),
        ('paid', 'مدفوع'),
        ('failed', 'فشل'),
        ('refunded', 'مسترد'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    order_number = models.CharField(max_length=20, unique=True, verbose_name="رقم الطلب")

    # معلومات الشحن
    shipping_name = models.CharField(max_length=100, verbose_name="اسم المستلم")
    shipping_phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    shipping_address = models.TextField(verbose_name="عنوان الشحن")
    shipping_city = models.CharField(max_length=50, verbose_name="المدينة")
    shipping_postal_code = models.CharField(max_length=10, blank=True, verbose_name="الرمز البريدي")

    # معلومات الطلب
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="حالة الطلب")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="حالة الدفع")

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المجموع الفرعي")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="تكلفة الشحن")
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="الضريبة")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ الإجمالي")

    notes = models.TextField(blank=True, verbose_name="ملاحظات")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب #{self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # إنشاء رقم طلب فريد
            import uuid
            self.order_number = f"VL{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """عناصر الطلب"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="الطلب")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")
    quantity = models.PositiveIntegerField(verbose_name="الكمية")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الإجمالي")

    class Meta:
        verbose_name = "عنصر طلب"
        verbose_name_plural = "عناصر الطلبات"

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)
