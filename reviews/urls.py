from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Reviews
    path('products/<slug:slug>/reviews/', views.ProductReviewsView.as_view(), name='product-reviews'),
    path('products/<slug:slug>/reviews/stats/', views.review_stats, name='review-stats'),
    path('create/', views.ReviewCreateView.as_view(), name='review-create'),

    # Contact
    path('contact/', views.ContactMessageCreateView.as_view(), name='contact-create'),
]