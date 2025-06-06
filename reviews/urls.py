from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/<int:product_id>/', views.AddReviewView.as_view(), name='add'),
    path('<int:pk>/edit/', views.EditReviewView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.DeleteReviewView.as_view(), name='delete'),
    path('<int:pk>/helpful/', views.MarkHelpfulView.as_view(), name='helpful'),
]
