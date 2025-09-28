# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # ============ CATEGORY URLs ============
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<slug:slug>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('categories/<slug:slug>/force-delete/', views.CategoryForceDeleteView.as_view(), name='category-force-delete'),
    path('categories/<slug:slug>/products/', views.CategoryProductsView.as_view(), name='category-products'),

    # ============ PRODUCT URLs ============
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/search/', views.ProductSearchView.as_view(), name='product-search'),
    path('products/featured/', views.FeaturedProductsView.as_view(), name='featured-products'),
    path('products/popular/', views.popular_products, name='popular-products'),
    path('products/latest/', views.latest_products, name='latest-products'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),

    # ============ UTILITY URLs ============
    path('filters-info/', views.product_filters_info, name='filters-info'),

    # ============ BULK DELETE URLs ============
    path('bulk-delete/products/', views.bulk_delete_products, name='bulk-delete-products'),
    path('bulk-delete/categories/', views.bulk_delete_categories, name='bulk-delete-categories'),
]