from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<slug:slug>/products/', views.CategoryProductsView.as_view(), name='category-products'),

    # Products
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('search/', views.ProductSearchView.as_view(), name='product-search'),

    # Special endpoints
    path('featured/', views.FeaturedProductsView.as_view(), name='featured-products'),
    path('popular/', views.popular_products, name='popular-products'),
    path('latest/', views.latest_products, name='latest-products'),
    path('filters/', views.product_filters_info, name='product-filters'),
]
