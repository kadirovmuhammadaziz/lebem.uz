from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/featured/', views.featured_products, name='featured-products'),
    path('products/cheap/', views.cheap_products, name='cheap-products'),
    path('products/expensive/', views.expensive_products, name='expensive-products'),
]