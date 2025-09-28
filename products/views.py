from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Product
from .serializers import CategorySerializer, CategoryDetailSerializer, ProductSerializer
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404


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


# Mahsulotni o'chirish uchun DestroyAPIView
class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Soft delete - mahsulotni faol emas deb belgilash
        instance.is_active = False
        instance.save()

        return Response(
            {'message': 'Mahsulot muvaffaqiyatli o\'chirildi'},
            status=status.HTTP_200_OK
        )


# Yoki function-based view sifatida
@api_view(['DELETE'])
def delete_product(request, slug):
    """Mahsulotni o'chirish (soft delete)"""
    try:
        product = Product.objects.get(slug=slug)
        # Soft delete
        product.is_active = False
        product.save()

        return Response({
            'success': True,
            'message': 'Mahsulot muvaffaqiyatli o\'chirildi'
        }, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Mahsulot topilmadi'
        }, status=status.HTTP_404_NOT_FOUND)


# Agar to'liq o'chirish kerak bo'lsa (hard delete)
@api_view(['DELETE'])
def hard_delete_product(request, slug):
    """Mahsulotni butunlay o'chirish (hard delete)"""
    try:
        product = Product.objects.get(slug=slug)
        product_name = product.name
        product.delete()  # Bazadan butunlay o'chirish

        return Response({
            'success': True,
            'message': f'{product_name} mahsuloti butunlay o\'chirildi'
        }, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Mahsulot topilmadi'
        }, status=status.HTTP_404_NOT_FOUND)


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


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(
            is_featured=True, is_active=True
        )[:8]  # tavsiya etilgan
        context['categories'] = Category.objects.filter(
            is_active=True
        )[:6]  # faqat 6 ta kategoriya chiqadi
        context['cheap_products'] = Product.objects.filter(
            is_active=True
        ).order_by('price')[:4]  # eng arzon 4 ta mahsulot
        return context


def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, slug):
    """Mahsulot batafsil sahifasi"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'products/product_detail.html', {'object': product})