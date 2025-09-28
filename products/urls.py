from django.urls import path
from . import views

urlpatterns = [
    # Web sahifalar
    path('', views.product_list, name='product-list-web'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),

    # API endpoints (DRF)
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail-api'),
    path('products/featured/', views.featured_products, name='featured-products'),
    path('products/cheap/', views.cheap_products, name='cheap-products'),
    path('products/expensive/', views.expensive_products, name='expensive-products'),
]
