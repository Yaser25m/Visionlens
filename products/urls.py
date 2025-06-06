from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('category/<int:category_id>/', views.CategoryProductsView.as_view(), name='category'),
    path('brand/<int:brand_id>/', views.BrandProductsView.as_view(), name='brand'),
    path('search/', views.ProductSearchView.as_view(), name='search'),
]
