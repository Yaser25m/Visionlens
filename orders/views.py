from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product


class CartView(View):
    """عرض سلة التسوق"""
    def get(self, request):
        cart = None
        cart_items = []

        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                cart_items = cart.items.select_related('product', 'product__brand').all()
            except Cart.DoesNotExist:
                cart = None
                cart_items = []

        context = {
            'cart_items': cart_items,
            'cart': cart,
        }
        return render(request, 'orders/cart.html', context)


class AddToCartView(LoginRequiredMixin, View):
    """إضافة منتج إلى السلة"""
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        try:
            product = get_object_or_404(Product, id=product_id, is_active=True)

            # التحقق من توفر المنتج
            if not product.is_in_stock:
                messages.error(request, 'هذا المنتج غير متوفر حالياً')
                return redirect('products:detail', pk=product_id)

            # التحقق من الكمية المطلوبة
            if quantity > product.stock_quantity:
                messages.error(request, f'الكمية المطلوبة غير متوفرة. الكمية المتاحة: {product.stock_quantity}')
                return redirect('products:detail', pk=product_id)

            cart, created = Cart.objects.get_or_create(user=request.user)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                new_quantity = cart_item.quantity + quantity
                if new_quantity > product.stock_quantity:
                    messages.error(request, f'لا يمكن إضافة هذه الكمية. الكمية المتاحة: {product.stock_quantity}')
                    return redirect('products:detail', pk=product_id)
                cart_item.quantity = new_quantity
                cart_item.save()

            # للطلبات AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'cart_count': cart.total_items,
                    'message': 'تم إضافة المنتج إلى السلة'
                })

            messages.success(request, 'تم إضافة المنتج إلى السلة بنجاح!')
            return redirect('orders:cart')

        except Exception as e:
            messages.error(request, 'حدث خطأ أثناء إضافة المنتج إلى السلة')
            return redirect('products:detail', pk=product_id)


class UpdateCartView(LoginRequiredMixin, View):
    """تحديث كمية منتج في السلة"""
    def post(self, request):
        import json

        try:
            data = json.loads(request.body)
            cart_item_id = data.get('cart_item_id')
            quantity = int(data.get('quantity', 1))

            cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

            # التحقق من الكمية المتاحة
            if quantity > cart_item.product.stock_quantity:
                return JsonResponse({
                    'success': False,
                    'message': f'الكمية المطلوبة غير متوفرة. الكمية المتاحة: {cart_item.product.stock_quantity}'
                })

            if quantity <= 0:
                cart_item.delete()
                cart = cart_item.cart
                return JsonResponse({
                    'success': True,
                    'item_total': '0 د.ع',
                    'cart_total': f'{cart.total_price} د.ع',
                    'cart_count': cart.total_items,
                    'item_removed': True
                })

            cart_item.quantity = quantity
            cart_item.save()

            cart = cart_item.cart

            return JsonResponse({
                'success': True,
                'item_total': f'{cart_item.total_price} د.ع',
                'cart_total': f'{cart.total_price} د.ع',
                'cart_count': cart.total_items
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'حدث خطأ أثناء تحديث السلة'
            })


class RemoveFromCartView(LoginRequiredMixin, View):
    """إزالة منتج من السلة"""
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()

        messages.success(request, 'تم إزالة المنتج من السلة')
        return redirect('orders:cart')


class CheckoutView(LoginRequiredMixin, View):
    """صفحة الدفع"""
    def get(self, request):
        # سيتم تنفيذها لاحقاً
        return render(request, 'orders/checkout.html')


class OrderListView(LoginRequiredMixin, ListView):
    """عرض قائمة الطلبات"""
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    """عرض تفاصيل الطلب"""
    model = Order
    template_name = 'orders/detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CancelOrderView(LoginRequiredMixin, View):
    """إلغاء الطلب"""
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)

        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.save()
            messages.success(request, 'تم إلغاء الطلب بنجاح')
        else:
            messages.error(request, 'لا يمكن إلغاء هذا الطلب')

        return redirect('orders:detail', pk=order.pk)
