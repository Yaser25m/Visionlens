from django.core.management.base import BaseCommand
from products.models import Category, Brand, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'إنشاء بيانات تجريبية للمتجر'

    def handle(self, *args, **options):
        self.stdout.write('إنشاء البيانات التجريبية...')

        # إنشاء الفئات
        categories_data = [
            {'name': 'عدسات يومية', 'name_en': 'Daily Lenses', 'description': 'عدسات لاصقة للاستخدام اليومي'},
            {'name': 'عدسات شهرية', 'name_en': 'Monthly Lenses', 'description': 'عدسات لاصقة للاستخدام الشهري'},
            {'name': 'عدسات تجميلية', 'name_en': 'Cosmetic Lenses', 'description': 'عدسات لاصقة ملونة للتجميل'},
            {'name': 'عدسات طبية', 'name_en': 'Medical Lenses', 'description': 'عدسات لاصقة لتصحيح النظر'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'تم إنشاء الفئة: {category.name}')

        # إنشاء العلامات التجارية
        brands_data = [
            {'name': 'Acuvue', 'description': 'علامة تجارية رائدة في العدسات اللاصقة'},
            {'name': 'Bausch + Lomb', 'description': 'شركة عالمية متخصصة في منتجات العيون'},
            {'name': 'CooperVision', 'description': 'مصنع عدسات لاصقة عالمي'},
            {'name': 'Alcon', 'description': 'شركة رائدة في مجال العناية بالعيون'},
            {'name': 'Freshlook', 'description': 'علامة تجارية مشهورة للعدسات الملونة'},
        ]

        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=brand_data['name'],
                defaults=brand_data
            )
            if created:
                self.stdout.write(f'تم إنشاء العلامة التجارية: {brand.name}')

        # إنشاء المنتجات
        daily_category = Category.objects.get(name='عدسات يومية')
        monthly_category = Category.objects.get(name='عدسات شهرية')
        cosmetic_category = Category.objects.get(name='عدسات تجميلية')
        medical_category = Category.objects.get(name='عدسات طبية')

        acuvue = Brand.objects.get(name='Acuvue')
        bausch = Brand.objects.get(name='Bausch + Lomb')
        cooper = Brand.objects.get(name='CooperVision')
        alcon = Brand.objects.get(name='Alcon')
        freshlook = Brand.objects.get(name='Freshlook')

        products_data = [
            # عدسات يومية
            {
                'name': 'أكيوفيو وان داي موست',
                'name_en': 'Acuvue 1-Day Moist',
                'description': 'عدسات لاصقة يومية مريحة ومرطبة للاستخدام اليومي',
                'description_en': 'Daily disposable contact lenses with moisture technology',
                'category': daily_category,
                'brand': acuvue,
                'price': Decimal('25000'),
                'lens_type': 'daily',
                'lens_usage': 'medical',
                'color': 'شفاف',
                'power': '-1.00 إلى -12.00',
                'diameter': '14.2 مم',
                'base_curve': '8.5 مم',
                'stock_quantity': 100,
                'is_featured': True,
            },
            {
                'name': 'أكيوفيو وان داي ترو آي',
                'name_en': 'Acuvue 1-Day TruEye',
                'description': 'عدسات يومية متقدمة مع تقنية السيليكون هيدروجيل',
                'description_en': 'Advanced daily lenses with silicone hydrogel technology',
                'category': daily_category,
                'brand': acuvue,
                'price': Decimal('35000'),
                'discount_price': Decimal('30000'),
                'lens_type': 'daily',
                'lens_usage': 'medical',
                'color': 'شفاف',
                'power': '-0.50 إلى -10.00',
                'diameter': '14.2 مم',
                'base_curve': '8.5 مم',
                'stock_quantity': 80,
                'is_featured': True,
            },
            
            # عدسات شهرية
            {
                'name': 'بايوفينيتي',
                'name_en': 'Biofinity',
                'description': 'عدسات شهرية مريحة للاستخدام المطول',
                'description_en': 'Monthly contact lenses for extended wear comfort',
                'category': monthly_category,
                'brand': cooper,
                'price': Decimal('45000'),
                'lens_type': 'monthly',
                'lens_usage': 'medical',
                'color': 'شفاف',
                'power': '-0.25 إلى -12.00',
                'diameter': '14.0 مم',
                'base_curve': '8.6 مم',
                'stock_quantity': 60,
                'is_featured': True,
            },
            {
                'name': 'إير أوبتكس أكوا',
                'name_en': 'Air Optix Aqua',
                'description': 'عدسات شهرية مع تقنية التنفس الفائق',
                'description_en': 'Monthly lenses with superior breathability technology',
                'category': monthly_category,
                'brand': alcon,
                'price': Decimal('50000'),
                'discount_price': Decimal('42000'),
                'lens_type': 'monthly',
                'lens_usage': 'medical',
                'color': 'شفاف',
                'power': '-0.50 إلى -10.00',
                'diameter': '14.2 مم',
                'base_curve': '8.6 مم',
                'stock_quantity': 40,
            },
            
            # عدسات تجميلية
            {
                'name': 'فريش لوك كولور بلندز',
                'name_en': 'FreshLook ColorBlends',
                'description': 'عدسات ملونة طبيعية المظهر',
                'description_en': 'Natural-looking colored contact lenses',
                'category': cosmetic_category,
                'brand': freshlook,
                'price': Decimal('55000'),
                'lens_type': 'monthly',
                'lens_usage': 'cosmetic',
                'color': 'أزرق',
                'power': '0.00 إلى -8.00',
                'diameter': '14.5 مم',
                'base_curve': '8.6 مم',
                'stock_quantity': 30,
                'is_featured': True,
            },
            {
                'name': 'فريش لوك كولور بلندز أخضر',
                'name_en': 'FreshLook ColorBlends Green',
                'description': 'عدسات ملونة باللون الأخضر الطبيعي',
                'description_en': 'Natural green colored contact lenses',
                'category': cosmetic_category,
                'brand': freshlook,
                'price': Decimal('55000'),
                'lens_type': 'monthly',
                'lens_usage': 'cosmetic',
                'color': 'أخضر',
                'power': '0.00 إلى -8.00',
                'diameter': '14.5 مم',
                'base_curve': '8.6 مم',
                'stock_quantity': 25,
            },
            {
                'name': 'فريش لوك كولور بلندز عسلي',
                'name_en': 'FreshLook ColorBlends Honey',
                'description': 'عدسات ملونة باللون العسلي الجذاب',
                'description_en': 'Attractive honey colored contact lenses',
                'category': cosmetic_category,
                'brand': freshlook,
                'price': Decimal('55000'),
                'discount_price': Decimal('48000'),
                'lens_type': 'monthly',
                'lens_usage': 'cosmetic',
                'color': 'عسلي',
                'power': '0.00 إلى -8.00',
                'diameter': '14.5 مم',
                'base_curve': '8.6 مم',
                'stock_quantity': 35,
            },
            
            # عدسات طبية متقدمة
            {
                'name': 'بيوفينيتي توريك',
                'name_en': 'Biofinity Toric',
                'description': 'عدسات شهرية لتصحيح الاستجماتيزم',
                'description_en': 'Monthly toric lenses for astigmatism correction',
                'category': medical_category,
                'brand': cooper,
                'price': Decimal('75000'),
                'lens_type': 'monthly',
                'lens_usage': 'medical',
                'color': 'شفاف',
                'power': '-0.75 إلى -6.00',
                'diameter': '14.5 مم',
                'base_curve': '8.7 مم',
                'stock_quantity': 20,
            },
            {
                'name': 'أكيوفيو أوازيس',
                'name_en': 'Acuvue Oasys',
                'description': 'عدسات أسبوعية مع تقنية الترطيب المتقدمة',
                'description_en': 'Weekly lenses with advanced hydration technology',
                'category': medical_category,
                'brand': acuvue,
                'price': Decimal('65000'),
                'discount_price': Decimal('58000'),
                'lens_type': 'weekly',
                'lens_usage': 'medical',
                'color': 'شفاف',
                'power': '-0.50 إلى -12.00',
                'diameter': '14.0 مم',
                'base_curve': '8.4 مم',
                'stock_quantity': 45,
                'is_featured': True,
            },
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'تم إنشاء المنتج: {product.name}')

        self.stdout.write(
            self.style.SUCCESS('تم إنشاء البيانات التجريبية بنجاح!')
        )
