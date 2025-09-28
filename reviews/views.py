# reviews/views.py
from django.conf import settings
from django.db.models import Count, Avg
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Review, ContactMessage
from .serializers import (
    ReviewSerializer, ReviewCreateSerializer, ReviewListSerializer,
    ContactMessageSerializer
)

# Telegram task import (agar mavjud bo'lsa)
try:
    from .tasks import send_telegram_notification
except ImportError:
    def send_telegram_notification(*args, **kwargs):
        pass


# ============ REVIEW VIEWS ============

class ProductReviewsView(generics.ListAPIView):
    """Mahsulot sharhlari"""
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        product_slug = self.kwargs.get('slug')
        return Review.objects.filter(
            product__slug=product_slug,
            product__is_active=True,
            is_active=True
        ).order_by('-created_at')


class ReviewCreateView(generics.CreateAPIView):
    """Sharh yaratish"""
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # IP addressni saqlash
        ip_address = self.get_client_ip(request)
        review = serializer.save(ip_address=ip_address)

        # Telegram orqali xabar yuborish
        try:
            send_telegram_notification.delay(
                message_type='review',
                data={
                    'name': review.name,
                    'phone': review.phone,
                    'product': review.product.name,
                    'rating': review.rating,
                    'comment': review.comment
                }
            )
        except:
            pass

        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ReviewDeleteView(generics.DestroyAPIView):
    """Sharhni o'chirish (soft delete)"""
    queryset = Review.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Soft delete
        instance.is_active = False
        instance.save(update_fields=['is_active'])

        return Response(
            {'message': 'Sharh muvaffaqiyatli o\'chirildi'},
            status=status.HTTP_204_NO_CONTENT
        )


class ReviewUpdateView(generics.UpdateAPIView):
    """Sharhni tahrirlash (admin uchun)"""
    queryset = Review.objects.filter(is_active=True)
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ReviewListView(generics.ListAPIView):
    """Barcha sharhlar (admin uchun)"""
    queryset = Review.objects.all().select_related('product').order_by('-created_at')
    serializer_class = ReviewListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Status bo'yicha filter
        status_filter = self.request.query_params.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)

        # Product bo'yicha filter
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        # Rating bo'yicha filter
        rating = self.request.query_params.get('rating')
        if rating:
            queryset = queryset.filter(rating=rating)

        return queryset


# ============ CONTACT MESSAGE VIEWS ============

class ContactMessageCreateView(generics.CreateAPIView):
    """Aloqa xabari yaratish"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # IP addressni saqlash
        ip_address = self.get_client_ip(request)
        message = serializer.save(ip_address=ip_address)

        # Telegram orqali xabar yuborish
        try:
            send_telegram_notification.delay(
                message_type='contact',
                data={
                    'name': message.name,
                    'phone': message.phone,
                    'email': message.email,
                    'subject': message.get_subject_display(),
                    'message': message.message
                }
            )
        except:
            pass

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ContactMessageListView(generics.ListAPIView):
    """Aloqa xabarlari ro'yxati (admin uchun)"""
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Subject bo'yicha filter
        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(subject=subject)

        # Sana oralig'i bo'yicha filter
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')

        if from_date:
            queryset = queryset.filter(created_at__gte=from_date)
        if to_date:
            queryset = queryset.filter(created_at__lte=to_date)

        return queryset


class ContactMessageDetailView(generics.RetrieveAPIView):
    """Aloqa xabari tafsilotlari (admin uchun)"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ContactMessageDeleteView(generics.DestroyAPIView):
    """Aloqa xabarini o'chirish"""
    queryset = ContactMessage.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()  # Hard delete for contact messages

        return Response(
            {'message': 'Aloqa xabari o\'chirildi'},
            status=status.HTTP_204_NO_CONTENT
        )


# ============ API VIEW FUNCTIONS ============

@api_view(['GET'])
def review_stats(request, slug):
    """Mahsulot sharhlari statistikasi"""
    reviews = Review.objects.filter(
        product__slug=slug,
        product__is_active=True,
        is_active=True
    )

    stats = reviews.aggregate(
        total_reviews=Count('id'),
        average_rating=Avg('rating')
    )

    rating_breakdown = reviews.values('rating').annotate(
        count=Count('rating')
    ).order_by('-rating')

    return Response({
        'total_reviews': stats['total_reviews'] or 0,
        'average_rating': round(stats['average_rating'] or 0, 2),
        'rating_breakdown': list(rating_breakdown)
    })


@api_view(['GET'])
def dashboard_stats(request):
    """Admin dashboard statistikalari"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(
            {'error': 'Ruxsat berilmagan'},
            status=status.HTTP_403_FORBIDDEN
        )

    from datetime import datetime, timedelta

    # So'nggi 30 kun ichidagi statistikalar
    thirty_days_ago = datetime.now() - timedelta(days=30)

    stats = {
        'reviews': {
            'total': Review.objects.filter(is_active=True).count(),
            'recent': Review.objects.filter(
                created_at__gte=thirty_days_ago,
                is_active=True
            ).count(),
            'by_rating': list(
                Review.objects.filter(is_active=True)
                .values('rating')
                .annotate(count=Count('rating'))
                .order_by('-rating')
            )
        },
        'contact_messages': {
            'total': ContactMessage.objects.count(),
            'recent': ContactMessage.objects.filter(
                created_at__gte=thirty_days_ago
            ).count(),
            'by_subject': list(
                ContactMessage.objects.values('subject')
                .annotate(count=Count('subject'))
                .order_by('-count')
            )
        }
    }

    return Response(stats)


@api_view(['POST'])
def bulk_delete_reviews(request):
    """Bir nechta sharhni bir vaqtda o'chirish"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(
            {'error': 'Ruxsat berilmagan'},
            status=status.HTTP_403_FORBIDDEN
        )

    review_ids = request.data.get('review_ids', [])
    if not review_ids:
        return Response(
            {'error': 'Sharh ID lari ko\'rsatilmagan'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Sharhlarni soft delete
    updated_count = Review.objects.filter(
        id__in=review_ids,
        is_active=True
    ).update(is_active=False)

    return Response({
        'message': f'{updated_count} ta sharh o\'chirildi',
        'deleted_count': updated_count
    })


@api_view(['POST'])
def bulk_delete_contacts(request):
    """Bir nechta aloqa xabarini bir vaqtda o'chirish"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(
            {'error': 'Ruxsat berilmagan'},
            status=status.HTTP_403_FORBIDDEN
        )

    contact_ids = request.data.get('contact_ids', [])
    if not contact_ids:
        return Response(
            {'error': 'Aloqa xabari ID lari ko\'rsatilmagan'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Aloqa xabarlarini hard delete
    deleted_count, _ = ContactMessage.objects.filter(
        id__in=contact_ids
    ).delete()

    return Response({
        'message': f'{deleted_count} ta aloqa xabari o\'chirildi',
        'deleted_count': deleted_count
    })


@api_view(['PATCH'])
def toggle_review_status(request, pk):
    """Sharh statusini o'zgartirish (faol/nofaol)"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(
            {'error': 'Ruxsat berilmagan'},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        review = Review.objects.get(pk=pk)
        review.is_active = not review.is_active
        review.save(update_fields=['is_active'])

        return Response({
            'message': f'Sharh {"faollashtirildi" if review.is_active else "nofaollashtirildi"}',
            'is_active': review.is_active
        })
    except Review.DoesNotExist:
        return Response(
            {'error': 'Sharh topilmadi'},
            status=status.HTTP_404_NOT_FOUND
        )