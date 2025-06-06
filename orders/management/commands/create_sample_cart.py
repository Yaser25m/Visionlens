from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from orders.models import Cart, CartItem
from products.models import Product


class Command(BaseCommand):
    help = 'إنشاء سلة تسوق تجريبية'

    def handle(self, *args, **options):
        self.stdout.write('إنشاء سلة تسوق تجريبية...')

        # البحث عن مستخدم موجود أو إنشاء مستخدم جديد
        try:
            user = User.objects.get(username='testuser')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123',
                first_name='مستخدم',
                last_name='تجريبي'
            )
            self.stdout.write(f'تم إنشاء المستخدم: {user.username}')

        # إنشاء أو الحصول على السلة
        cart, created = Cart.objects.get_or_create(user=user)
        if created:
            self.stdout.write(f'تم إنشاء سلة جديدة للمستخدم: {user.username}')
        else:
            # مسح السلة الموجودة
            cart.items.all().delete()
            self.stdout.write(f'تم مسح السلة الموجودة للمستخدم: {user.username}')

        # إضافة منتجات إلى السلة
        products_to_add = [
            {'name': 'أكيوفيو وان داي موست', 'quantity': 2},
            {'name': 'فريش لوك كولور بلندز', 'quantity': 1},
            {'name': 'بايوفينيتي', 'quantity': 3},
        ]

        for item_data in products_to_add:
            try:
                product = Product.objects.get(name=item_data['name'])
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': item_data['quantity']}
                )
                if created:
                    self.stdout.write(f'تم إضافة {product.name} إلى السلة - الكمية: {item_data["quantity"]}')
                else:
                    cart_item.quantity = item_data['quantity']
                    cart_item.save()
                    self.stdout.write(f'تم تحديث {product.name} في السلة - الكمية: {item_data["quantity"]}')
            except Product.DoesNotExist:
                self.stdout.write(f'المنتج غير موجود: {item_data["name"]}')

        self.stdout.write(
            self.style.SUCCESS(f'تم إنشاء سلة تجريبية بنجاح! إجمالي العناصر: {cart.total_items}, إجمالي السعر: {cart.total_price} د.ع')
        )
        self.stdout.write(f'يمكنك تسجيل الدخول باستخدام: testuser / testpass123')
