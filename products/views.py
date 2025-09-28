from django.db.models import Q, F, Min, Max
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Category, Product
from .serializers import (
    CategorySerializer, CategoryListSerializer, ProductListSerializer,
    ProductDetailSerializer, ProductSearchSerializer
)


# ============ CATEGORY VIEWS ============

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


class CategoryDeleteView(generics.DestroyAPIView):
    """Kategoriyani o'chirish (soft delete)"""
    queryset = Category.objects.filter(is_active=True)
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Kategoriya ichidagi mahsulotlar sonini tekshirish
        products_count = Product.objects.filter(category=instance, is_active=True).count()

        if products_count > 0:
            return Response(
                {
                    'error': f'Kategoriyani o\'chirish mumkin emas. Ichida {products_count} ta faol mahsulot mavjud.',
                    'products_count': products_count
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Soft delete
        instance.is_active = False
        instance.save(update_fields=['is_active'])

        return Response(
            {'message': 'Kategoriya muvaffaqiyatli o\'chirildi'},
            status=status.HTTP_204_NO_CONTENT
        )


class CategoryForceDeleteView(generics.DestroyAPIView):
    """Kategoriyani majburiy o'chirish (barcha mahsulotlar bilan birga)"""
    queryset = Category.objects.filter(is_active=True)
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Kategoriya ichidagi barcha mahsulotlarni ham o'chirish
        products = Product.objects.filter(category=instance, is_active=True)
        products_count = products.count()

        # Mahsulotlarni soft delete
        products.update(is_active=False)

        # Kategoriyani soft delete
        instance.is_active = False
        instance.save(update_fields=['is_active'])

        return Response(
            {
                'message': f'Kategoriya va uning ichidagi {products_count} ta mahsulot o\'chirildi',
                'deleted_products_count': products_count
            },
            status=status.HTTP_204_NO_CONTENT
        )


# ============ PRODUCT VIEWS ============

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


class ProductDeleteView(generics.DestroyAPIView):
    """Mahsulotni o'chirish (soft delete)"""
    queryset = Product.objects.filter(is_active=True)
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Mahsulot sharhlarini ham tekshirish (agar reviews app bilan bog'langan bo'lsa)
        try:
            from reviews.models import Review
            reviews_count = Review.objects.filter(product=instance, is_active=True).count()
        except ImportError:
            reviews_count = 0

        # Soft delete
        instance.is_active = False
        instance.save(update_fields=['is_active'])

        # Mahsulot sharhlarini ham o'chirish (agar reviews app bilan bog'langan bo'lsa)
        if reviews_count > 0:
            try:
                Review.objects.filter(product=instance).update(is_active=False)
            except:
                pass

        return Response(
            {
                'message': 'Mahsulot muvaffaqiyatli o\'chirildi',
                'deleted_reviews_count': reviews_count
            },
            status=status.HTTP_204_NO_CONTENT
        )


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


# ============ API VIEW FUNCTIONS ============

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


# ============ BULK DELETE VIEWS ============

@api_view(['POST'])
def bulk_delete_products(request):
    """Bir nechta mahsulotni bir vaqtda o'chirish"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(
            {'error': 'Ruxsat berilmagan'},
            status=status.HTTP_403_FORBIDDEN
        )

    product_ids = request.data.get('product_ids', [])
    if not product_ids:
        return Response(
            {'error': 'Mahsulot ID lari ko\'rsatilmagan'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Mahsulotlarni soft delete
    updated_count = Product.objects.filter(
        id__in=product_ids,
        is_active=True
    ).update(is_active=False)

    # Bog'liq sharhlarni ham o'chirish (agar reviews app bor bo'lsa)
    try:
        from reviews.models import Review
        Review.objects.filter(
            product_id__in=product_ids
        ).update(is_active=False)
    except ImportError:
        pass

    return Response({
        'message': f'{updated_count} ta mahsulot o\'chirildi',
        'deleted_count': updated_count
    })


@api_view(['POST'])
def bulk_delete_categories(request):
    """Bir nechta kategoriyani bir vaqtda o'chirish"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(
            {'error': 'Ruxsat berilmagan'},
            status=status.HTTP_403_FORBIDDEN
        )

    category_ids = request.data.get('category_ids', [])
    force_delete = request.data.get('force_delete', False)

    if not category_ids:
        return Response(
            {'error': 'Kategoriya ID lari ko\'rsatilmagan'},
            status=status.HTTP_400_BAD_REQUEST
        )

    categories = Category.objects.filter(id__in=category_ids, is_active=True)

    if not force_delete:
        # Kategoriyalar ichida mahsulot bor-yo'qligini tekshirish
        categories_with_products = categories.filter(
            product__is_active=True
        ).distinct()

        if categories_with_products.exists():
            return Response(
                {
                    'error': 'Ba\'zi kategoriyalar ichida faol mahsulotlar mavjud',
                    'categories_with_products': list(
                        categories_with_products.values_list('name', flat=True)
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    # Agar force_delete=True bo'lsa, avval mahsulotlarni o'chirish
    if force_delete:
        Product.objects.filter(
            category_id__in=category_ids,
            is_active=True
        ).update(is_active=False)

    # Kategoriyalarni soft delete
    updated_count = categories.update(is_active=False)

    return Response({
        'message': f'{updated_count} ta kategoriya o\'chirildi',
        'deleted_count': updated_count
    })