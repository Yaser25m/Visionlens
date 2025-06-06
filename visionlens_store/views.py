from django.shortcuts import render
from products.models import Product, Category, Brand
from reviews.models import Review


def home(request):
    """الصفحة الرئيسية"""
    # المنتجات المميزة
    featured_products = Product.objects.filter(
        is_active=True, 
        is_featured=True,
        stock_quantity__gt=0
    )[:8]
    
    # أحدث المنتجات
    latest_products = Product.objects.filter(
        is_active=True,
        stock_quantity__gt=0
    ).order_by('-created_at')[:8]
    
    # الفئات الرئيسية
    categories = Category.objects.filter(is_active=True)[:6]
    
    # العلامات التجارية
    brands = Brand.objects.filter(is_active=True)[:8]
    
    # أحدث التقييمات
    latest_reviews = Review.objects.filter(
        is_approved=True
    ).select_related('user', 'product').order_by('-created_at')[:6]
    
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,
        'brands': brands,
        'latest_reviews': latest_reviews,
    }
    
    return render(request, 'home.html', context)
