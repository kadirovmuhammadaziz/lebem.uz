from rest_framework import serializers
from .models import Review, ContactMessage
from products.models import Product


class ReviewSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'product', 'product_name', 'name', 'phone',
            'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'product_name']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'name', 'phone', 'rating', 'comment']

    def validate_product(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Bu mahsulot faol emas.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Baho 1 dan 5 gacha bo'lishi kerak.")
        return value

    def validate_phone(self, value):
        if not value.startswith('+998'):
            raise serializers.ValidationError(
                "Telefon raqam +998 bilan boshlanishi kerak."
            )
        return value


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id', 'name', 'rating', 'comment', 'created_at'
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'phone', 'email', 'subject',
            'message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_phone(self, value):
        if not value.startswith('+998'):
            raise serializers.ValidationError(
                "Telefon raqam +998 bilan boshlanishi kerak."
            )
        return value