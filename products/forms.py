from django import forms
from .models import Product, Category, Brand


class ProductAdminForm(forms.ModelForm):
    """نموذج مخصص لإدارة المنتجات"""
    
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'brand': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'name_en': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'description_en': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'discount_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'min_stock_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'lens_type': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'lens_usage': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'power': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'diameter': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
            'base_curve': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'style': 'width: 100%; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 8px;'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # التأكد من تحميل البيانات للقوائم المنسدلة
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        self.fields['brand'].queryset = Brand.objects.filter(is_active=True)
        
        # إضافة خيار فارغ
        self.fields['category'].empty_label = "اختر الفئة"
        self.fields['brand'].empty_label = "اختر العلامة التجارية"
        
        # تحسين عرض الخيارات
        self.fields['category'].widget.attrs.update({
            'data-placeholder': 'اختر الفئة',
            'required': True
        })
        self.fields['brand'].widget.attrs.update({
            'data-placeholder': 'اختر العلامة التجارية',
            'required': True
        })
    
    def clean_category(self):
        """التحقق من صحة الفئة"""
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('يجب اختيار فئة للمنتج')
        if not category.is_active:
            raise forms.ValidationError('الفئة المختارة غير نشطة')
        return category
    
    def clean_brand(self):
        """التحقق من صحة العلامة التجارية"""
        brand = self.cleaned_data.get('brand')
        if not brand:
            raise forms.ValidationError('يجب اختيار علامة تجارية للمنتج')
        if not brand.is_active:
            raise forms.ValidationError('العلامة التجارية المختارة غير نشطة')
        return brand
    
    def clean_price(self):
        """التحقق من صحة السعر"""
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('يجب أن يكون السعر أكبر من صفر')
        return price
    
    def clean_stock_quantity(self):
        """التحقق من صحة كمية المخزون"""
        stock = self.cleaned_data.get('stock_quantity')
        if stock and stock < 0:
            raise forms.ValidationError('لا يمكن أن تكون كمية المخزون سالبة')
        return stock
