from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.ReviewCreateView.as_view(), name='review-create'),
]
