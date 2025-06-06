from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg
from .models import Product, Category, Brand


class ProductListView(ListView):
    """عرض قائمة المنتجات"""
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True, stock_quantity__gt=0)

        # البحث
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(brand__name__icontains=query)
            )

        # فلترة حسب الفئة
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # فلترة حسب العلامة التجارية
        brand_id = self.request.GET.get('brand')
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        # فلترة حسب نوع العدسة
        lens_type = self.request.GET.get('lens_type')
        if lens_type:
            queryset = queryset.filter(lens_type=lens_type)

        # فلترة حسب استخدام العدسة
        lens_usage = self.request.GET.get('lens_usage')
        if lens_usage:
            queryset = queryset.filter(lens_usage=lens_usage)

        # فلترة حسب السعر
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # الترتيب
        sort_by = self.request.GET.get('sort', 'name')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'rating':
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        else:
            queryset = queryset.order_by('name')

        return queryset.select_related('category', 'brand').prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['brands'] = Brand.objects.filter(is_active=True)
        context['current_category'] = self.request.GET.get('category')
        context['current_brand'] = self.request.GET.get('brand')
        context['current_sort'] = self.request.GET.get('sort', 'name')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ProductDetailView(DetailView):
    """عرض تفاصيل المنتج"""
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category', 'brand').prefetch_related('images', 'reviews__user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # المنتجات المشابهة
        related_products = Product.objects.filter(
            category=product.category,
            is_active=True,
            stock_quantity__gt=0
        ).exclude(id=product.id)[:4]

        context['related_products'] = related_products

        # التقييمات
        reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
        context['reviews'] = reviews
        context['reviews_count'] = reviews.count()

        if reviews.exists():
            context['average_rating'] = reviews.aggregate(Avg('rating'))['rating__avg']
        else:
            context['average_rating'] = 0

        return context


class CategoryProductsView(ProductListView):
    """عرض منتجات فئة معينة"""
    template_name = 'products/category.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'], is_active=True)
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class BrandProductsView(ProductListView):
    """عرض منتجات علامة تجارية معينة"""
    template_name = 'products/brand.html'

    def get_queryset(self):
        self.brand = get_object_or_404(Brand, id=self.kwargs['brand_id'], is_active=True)
        return super().get_queryset().filter(brand=self.brand)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = self.brand
        return context


class ProductSearchView(ProductListView):
    """البحث في المنتجات"""
    template_name = 'products/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_performed'] = bool(self.request.GET.get('q'))
        return context
