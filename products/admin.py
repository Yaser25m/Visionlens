from django.contrib import admin
from django.shortcuts import redirect
from .models import Category, Brand, Product, ProductImage
from .forms import ProductAdminForm


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    max_num = 5
    fields = ('image', 'alt_text', 'is_primary')
    classes = ('collapse',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'name_en': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # form = ProductAdminForm  # مؤقتاً معطل
    list_display = ['image_preview', 'name', 'brand', 'category', 'price', 'discount_price', 'stock_quantity', 'images_count', 'is_active', 'is_featured']
    list_filter = ['brand', 'category', 'lens_type', 'lens_usage', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'name_en', 'description']
    prepopulated_fields = {'name_en': ('name',)}
    # inlines = [ProductImageInline]  # معطل نهائياً - استخدم إدارة الصور المنفصلة

    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('name', 'name_en', 'description', 'description_en', 'category', 'brand')
        }),
        ('الصورة الرئيسية', {
            'fields': ('main_image',),
            'description': 'ارفع الصورة الرئيسية للمنتج. يمكن إضافة صور إضافية لاحقاً من قسم "إدارة الصور".'
        }),
        ('التسعير', {
            'fields': ('price', 'discount_price')
        }),
        ('تفاصيل العدسة', {
            'fields': ('lens_type', 'lens_usage', 'color', 'power', 'diameter', 'base_curve')
        }),
        ('المخزون', {
            'fields': ('stock_quantity', 'min_stock_level')
        }),
        ('الحالة', {
            'fields': ('is_active', 'is_featured')
        }),
    )



    def add_view(self, request, form_url='', extra_context=None):
        """
        تخصيص عرض الإضافة
        """
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False

        # التأكد من تحميل البيانات للقوائم المنسدلة
        from .models import Category, Brand
        extra_context['categories'] = Category.objects.filter(is_active=True)
        extra_context['brands'] = Brand.objects.filter(is_active=True)

        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        تخصيص عرض التعديل
        """
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False

        # التأكد من تحميل البيانات للقوائم المنسدلة
        from .models import Category, Brand
        extra_context['categories'] = Category.objects.filter(is_active=True)
        extra_context['brands'] = Brand.objects.filter(is_active=True)

        return super().change_view(request, object_id, form_url, extra_context)

    def image_preview(self, obj):
        """معاينة الصورة الرئيسية"""
        if obj.main_image:
            return f'<img src="{obj.main_image.url}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px; border: 1px solid #ddd;">'
        else:
            # البحث عن صورة رئيسية من الصور المضافة
            primary_image = obj.images.filter(is_primary=True).first()
            if primary_image:
                return f'<img src="{primary_image.image.url}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px; border: 1px solid #ddd; opacity: 0.7;">'
            else:
                return '<div style="width: 50px; height: 50px; background: #f0f0f0; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-size: 20px;">📷</div>'
    image_preview.short_description = "الصورة"
    image_preview.allow_tags = True

    def images_count(self, obj):
        """عدد صور المنتج مع روابط سريعة"""
        count = obj.images.count()
        if count > 0:
            # رابط لعرض صور هذا المنتج
            view_url = f"/admin/products/productimage/?product__id__exact={obj.id}"
            # رابط لإضافة صورة جديدة
            add_url = f"/admin/products/productimage/add/?product={obj.id}"
            return f'''
                <div style="display: flex; gap: 5px; align-items: center;">
                    <a href="{view_url}" style="color: #007cba; font-weight: bold; text-decoration: none;">
                        📷 {count} صورة
                    </a>
                    <a href="{add_url}" style="color: #28a745; font-size: 16px; text-decoration: none;" title="إضافة صورة جديدة">
                        ➕
                    </a>
                </div>
            '''
        else:
            add_url = f"/admin/products/productimage/add/?product={obj.id}"
            return f'''
                <a href="{add_url}" style="color: #e74c3c; font-weight: bold; text-decoration: none;">
                    📷 إضافة صور
                </a>
            '''
    images_count.short_description = "إدارة الصور"
    images_count.allow_tags = True




@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'alt_text', 'is_primary', 'created_at', 'quick_actions']
    list_filter = ['is_primary', 'created_at', 'product__category', 'product__brand']
    search_fields = ['product__name', 'alt_text']
    list_select_related = ['product']
    list_per_page = 20

    fieldsets = (
        ('معلومات الصورة', {
            'fields': ('product', 'image', 'alt_text', 'is_primary'),
            'description': 'ارفع صورة المنتج وأضف وصف مناسب. حدد "صورة رئيسية" للصورة الأساسية للمنتج.'
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        """تخصيص النموذج"""
        form = super().get_form(request, obj, **kwargs)

        # إذا تم تمرير معرف المنتج في URL، قم بتحديده مسبقاً
        if 'product' in request.GET:
            try:
                product_id = int(request.GET['product'])
                form.base_fields['product'].initial = product_id
                form.base_fields['product'].widget.attrs['readonly'] = True
            except (ValueError, TypeError):
                pass

        return form

    def image_preview(self, obj):
        """معاينة الصورة في قائمة الإدارة"""
        if obj.image:
            return f'<img src="{obj.image.url}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;">'
        return "لا توجد صورة"
    image_preview.short_description = "معاينة"
    image_preview.allow_tags = True

    def quick_actions(self, obj):
        """إجراءات سريعة للصورة"""
        actions = []

        if not obj.is_primary:
            actions.append(f'<a href="#" onclick="makePrimary({obj.id})" style="color: #28a745; text-decoration: none;" title="جعل رئيسية">⭐</a>')
        else:
            actions.append('<span style="color: #ffc107;" title="صورة رئيسية">⭐</span>')

        actions.append(f'<a href="/admin/products/productimage/{obj.id}/change/" style="color: #007cba; text-decoration: none;" title="تعديل">✏️</a>')
        actions.append(f'<a href="/admin/products/productimage/{obj.id}/delete/" style="color: #dc3545; text-decoration: none;" title="حذف">🗑️</a>')

        return ' '.join(actions)
    quick_actions.short_description = "إجراءات"
    quick_actions.allow_tags = True

    def save_model(self, request, obj, form, change):
        """حفظ النموذج مع التحقق من الصورة الرئيسية"""
        # إذا تم تحديد هذه الصورة كرئيسية، قم بإلغاء تحديد الصور الأخرى
        if obj.is_primary:
            ProductImage.objects.filter(product=obj.product, is_primary=True).update(is_primary=False)
        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        """إعادة توجيه بعد الإضافة"""
        if '_addanother' not in request.POST:
            # العودة لقائمة صور نفس المنتج
            return redirect(f'/admin/products/productimage/?product__id__exact={obj.product.id}')
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        """إعادة توجيه بعد التعديل"""
        if '_continue' not in request.POST and '_addanother' not in request.POST:
            # العودة لقائمة صور نفس المنتج
            return redirect(f'/admin/products/productimage/?product__id__exact={obj.product.id}')
        return super().response_change(request, obj)
