from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('products/', views.products_management, name='products'),
    path('orders/', views.orders_management, name='orders'),
]
