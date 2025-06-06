from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product


class Review(models.Model):
    """تقييمات المنتجات"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name="المنتج")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="التقييم"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان التقييم")
    comment = models.TextField(verbose_name="التعليق")
    is_verified_purchase = models.BooleanField(default=False, verbose_name="شراء موثق")
    is_approved = models.BooleanField(default=True, verbose_name="معتمد")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التقييم")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "تقييم"
        verbose_name_plural = "التقييمات"
        ordering = ['-created_at']
        unique_together = ('user', 'product')

    def __str__(self):
        return f"تقييم {self.user.username} لـ {self.product.name}"


class ReviewHelpful(models.Model):
    """تقييم مفيد"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    review = models.ForeignKey(Review, related_name='helpful_votes', on_delete=models.CASCADE, verbose_name="التقييم")
    is_helpful = models.BooleanField(verbose_name="مفيد")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التصويت")

    class Meta:
        verbose_name = "تصويت مفيد"
        verbose_name_plural = "التصويتات المفيدة"
        unique_together = ('user', 'review')

    def __str__(self):
        return f"تصويت {self.user.username} على تقييم {self.review.id}"
