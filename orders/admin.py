from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'cart_items_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username']
    # inlines = [CartItemInline]  # معطل لحل مشكلة النماذج المضمنة

    def total_items(self, obj):
        return obj.total_items
    total_items.short_description = 'عدد العناصر'

    def total_price(self, obj):
        return f"{obj.total_price} د.ع"
    total_price.short_description = 'السعر الإجمالي'

    def cart_items_count(self, obj):
        """عدد عناصر السلة مع رابط للإدارة"""
        count = obj.items.count()
        if count > 0:
            url = f"/admin/orders/cartitem/?cart__id__exact={obj.id}"
            return f'<a href="{url}" style="color: #007cba; font-weight: bold;">📦 {count} عنصر</a>'
        else:
            return '<span style="color: #999;">فارغة</span>'
    cart_items_count.short_description = "العناصر"
    cart_items_count.allow_tags = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total_amount', 'order_items_count', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'shipping_name']
    # inlines = [OrderItemInline]  # معطل لحل مشكلة النماذج المضمنة
    readonly_fields = ['order_number', 'created_at', 'updated_at']

    fieldsets = (
        ('معلومات الطلب', {
            'fields': ('order_number', 'user', 'status', 'payment_status', 'created_at', 'updated_at')
        }),
        ('معلومات الشحن', {
            'fields': ('shipping_name', 'shipping_phone', 'shipping_address', 'shipping_city', 'shipping_postal_code')
        }),
        ('المبالغ', {
            'fields': ('subtotal', 'shipping_cost', 'tax_amount', 'total_amount')
        }),
        ('ملاحظات', {
            'fields': ('notes',)
        }),
    )

    def order_items_count(self, obj):
        """عدد عناصر الطلب مع رابط للإدارة"""
        count = obj.items.count()
        if count > 0:
            url = f"/admin/orders/orderitem/?order__id__exact={obj.id}"
            return f'<a href="{url}" style="color: #007cba; font-weight: bold;">📦 {count} عنصر</a>'
        else:
            return '<span style="color: #999;">لا توجد عناصر</span>'
    order_items_count.short_description = "العناصر"
    order_items_count.allow_tags = True
