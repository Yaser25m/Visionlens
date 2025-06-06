from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('addresses/', views.AddressListView.as_view(), name='addresses'),
    path('addresses/add/', views.AddAddressView.as_view(), name='add_address'),
    path('addresses/<int:pk>/edit/', views.EditAddressView.as_view(), name='edit_address'),
    path('addresses/<int:pk>/delete/', views.DeleteAddressView.as_view(), name='delete_address'),
]
