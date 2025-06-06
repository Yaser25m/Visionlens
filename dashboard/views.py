from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.core.paginator import Paginator

from products.models import Product, Category, Brand
from orders.models import Order, OrderItem
from accounts.models import UserProfile
from reviews.models import Review
from .models import DashboardSettings, AdminActivity
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse


def admin_index_view(request, extra_context=None):
    """عرض مخصص لصفحة Admin الرئيسية مع الإحصائيات"""

    # إحصائيات سريعة
    products_count = Product.objects.count()
    orders_count = Order.objects.count()
    users_count = User.objects.filter(is_active=True).count()
    reviews_count = Review.objects.count()

    context = {
        'products_count': products_count,
        'orders_count': orders_count,
        'users_count': users_count,
        'reviews_count': reviews_count,
    }

    if extra_context:
        context.update(extra_context)

    return TemplateResponse(request, 'admin/index.html', context)


@staff_member_required
def dashboard_home(request):
    """الصفحة الرئيسية للوحة التحكم"""

    # إحصائيات عامة
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.filter(is_active=True).count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # إحصائيات هذا الشهر
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_orders = Order.objects.filter(created_at__gte=current_month).count()
    monthly_revenue = Order.objects.filter(
        created_at__gte=current_month,
        status='delivered'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # الطلبات الحديثة
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]

    # المنتجات الأكثر مبيعاً
    top_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).filter(total_sold__isnull=False).order_by('-total_sold')[:5]

    # المنتجات منخفضة المخزون
    low_stock_products = Product.objects.filter(
        stock_quantity__lte=10,
        is_active=True
    ).order_by('stock_quantity')[:5]

    # إحصائيات الطلبات حسب الحالة
    order_stats = Order.objects.values('status').annotate(count=Count('id'))

    # الأنشطة الحديثة
    recent_activities = AdminActivity.objects.select_related('user').order_by('-timestamp')[:10]

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'monthly_orders': monthly_orders,
        'monthly_revenue': monthly_revenue,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'low_stock_products': low_stock_products,
        'order_stats': order_stats,
        'recent_activities': recent_activities,
    }

    return render(request, 'dashboard/home.html', context)


@staff_member_required
def products_management(request):
    """إدارة المنتجات"""
    products_list = Product.objects.select_related('category', 'brand').order_by('-created_at')

    # البحث والفلترة
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    brand_filter = request.GET.get('brand', '')
    status_filter = request.GET.get('status', '')

    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if category_filter:
        products_list = products_list.filter(category_id=category_filter)

    if brand_filter:
        products_list = products_list.filter(brand_id=brand_filter)

    if status_filter:
        if status_filter == 'active':
            products_list = products_list.filter(is_active=True)
        elif status_filter == 'inactive':
            products_list = products_list.filter(is_active=False)
        elif status_filter == 'low_stock':
            products_list = products_list.filter(stock_quantity__lte=10)

    # التصفح
    paginator = Paginator(products_list, 20)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    # البيانات للفلاتر
    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'search_query': search_query,
        'category_filter': category_filter,
        'brand_filter': brand_filter,
        'status_filter': status_filter,
    }

    return render(request, 'dashboard/products.html', context)


@staff_member_required
def orders_management(request):
    """إدارة الطلبات"""
    orders_list = Order.objects.select_related('user').order_by('-created_at')

    # البحث والفلترة
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')

    if search_query:
        orders_list = orders_list.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(id__icontains=search_query)
        )

    if status_filter:
        orders_list = orders_list.filter(status=status_filter)

    if date_filter:
        if date_filter == 'today':
            orders_list = orders_list.filter(created_at__date=timezone.now().date())
        elif date_filter == 'week':
            week_ago = timezone.now() - timedelta(days=7)
            orders_list = orders_list.filter(created_at__gte=week_ago)
        elif date_filter == 'month':
            month_ago = timezone.now() - timedelta(days=30)
            orders_list = orders_list.filter(created_at__gte=month_ago)

    # التصفح
    paginator = Paginator(orders_list, 20)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    context = {
        'orders': orders,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'order_statuses': Order.STATUS_CHOICES,
    }

    return render(request, 'dashboard/orders.html', context)
