from django.db.models import Q, F, Min, Max
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Product
from .serializers import (
    CategorySerializer, CategoryListSerializer, ProductListSerializer,
    ProductDetailSerializer, ProductSearchSerializer
)


class CategoryListView(generics.ListAPIView):
    """Kategoriyalar ro'yxati"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        return super().get_queryset().order_by('sort_order', 'name')


class CategoryDetailView(generics.RetrieveAPIView):
    """Kategoriya tafsilotlari"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ProductListView(generics.ListAPIView):
    """Mahsulotlar ro'yxati"""
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['price', 'created_at', 'rating', 'views_count']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Category bo'yicha filter
        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Narx oralig'i bo'yicha filter
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Chegirma bor mahsulotlar
        has_discount = self.request.query_params.get('has_discount')
        if has_discount == 'false':
            queryset = queryset.filter(
                Q(old_price__lte=F('price')) | Q(old_price=0)
            )

        # Reyting bo'yicha filter
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """Mahsulot tafsilotlari"""
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Ko'rishlar sonini oshirish
        instance.views_count += 1
        instance.save(update_fields=['views_count'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FeaturedProductsView(generics.ListAPIView):
    """Tanlanган mahsulotlar"""
    queryset = Product.objects.filter(is_active=True, is_featured=True).select_related('category')
    serializer_class = ProductListSerializer
    ordering = ['-created_at']


class CategoryProductsView(generics.ListAPIView):
    """Kategoriya bo'yicha mahsulotlar"""
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['price', 'created_at', 'rating']
    ordering = ['price']  # Default: arzon narxdan boshlab

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        return Product.objects.filter(
            category__slug=category_slug,
            is_active=True,
            category__is_active=True
        ).select_related('category')


class ProductSearchView(generics.ListAPIView):
    """Mahsulot qidiruvi"""
    serializer_class = ProductSearchSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'short_description', 'category__name']
    ordering_fields = ['price', 'created_at', 'rating']
    ordering = ['price']

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category')


@api_view(['GET'])
def product_filters_info(request):
    """Mahsulot filterlash uchun ma'lumotlar"""
    products = Product.objects.filter(is_active=True)

    price_range = products.aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )

    return Response({
        'price_range': price_range,
        'categories': CategoryListSerializer(
            Category.objects.filter(is_active=True),
            many=True
        ).data
    })


@api_view(['GET'])
def popular_products(request):
    """Ommabop mahsulotlar (ko'p ko'rilganlar)"""
    products = Product.objects.filter(is_active=True).order_by('-views_count')[:10]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def latest_products(request):
    """Yangi mahsulotlar"""
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:10]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)