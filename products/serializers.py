from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductSpecification


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'image',
            'products_count', 'is_active', 'created_at'
        ]


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'products_count']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['id', 'name', 'value']


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)
    discount_percentage = serializers.ReadOnlyField()
    main_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'price',
            'old_price', 'discount_percentage', 'main_image',
            'category', 'rating', 'reviews_count', 'is_featured'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    discount_percentage = serializers.ReadOnlyField()
    reviews_count = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'price', 'old_price', 'discount_percentage', 'main_image',
            'category', 'images', 'specifications', 'rating',
            'reviews_count', 'views_count', 'is_featured', 'created_at'
        ]


class ProductSearchSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)
    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'price',
            'old_price', 'discount_percentage', 'main_image',
            'category', 'rating'
        ]