from rest_framework import generics, status
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from utils.telegram_bot import send_review_to_telegram, send_review_to_admin


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        # Telegram botga yuborish
        try:
            # Userga tasdiqlash xabari
            send_review_to_telegram(review)
            # Adminga xabar yuborish
            send_review_to_admin(review)
        except Exception as e:
            print(f"Telegram yuborishda xato: {e}")

        return Response(
            {'message': 'Izohingiz muvaffaqiyatli yuborildi!', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )