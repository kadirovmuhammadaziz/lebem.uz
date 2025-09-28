from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Product
from .serializers import CategorySerializer, CategoryDetailSerializer, ProductSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryDetailSerializer
    lookup_field = 'slug'


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['price']  # Default ordering by price (arzon narx birinchi)

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')

        # Kategoriya bo'yicha filterlash
        category_slug = self.request.query_params.get('category_slug', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Narx oralig'i bo'yicha filterlash
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'


@api_view(['GET'])
def featured_products(request):
    """Tavsiya etilgan mahsulotlar"""
    products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def cheap_products(request):
    """Eng arzon mahsulotlar"""
    products = Product.objects.filter(is_active=True).order_by('price')[:10]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def expensive_products(request):
    """Eng qimmat mahsulotlar"""
    products = Product.objects.filter(is_active=True).order_by('-price')[:10]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
