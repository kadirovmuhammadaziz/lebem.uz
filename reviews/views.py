from django.conf import settings
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Review, ContactMessage
from .serializers import (
    ReviewSerializer, ReviewCreateSerializer, ReviewListSerializer,
    ContactMessageSerializer
)
from .tasks import send_telegram_notification


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


@api_view(['GET'])
def review_stats(request, slug):
    """Mahsulot sharhlari statistikasi"""
    from django.db.models import Count, Avg

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