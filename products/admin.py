from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import Category, Product, ProductImage, ProductSpecification


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = [
        'name', 'slug', 'products_count', 'is_active',
        'sort_order', 'image_preview', 'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'sort_order']
    readonly_fields = ['image_preview', 'products_count']

    fieldsets = (
        (_('Asosiy ma\'lumotlar'), {
            'fields': ('name', 'slug', 'description', 'image', 'image_preview')
        }),
        (_('Sozlamalar'), {
            'fields': ('is_active', 'sort_order')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return _("Rasm yo'q")

    image_preview.short_description = _("Rasm ko'rinishi")

    def products_count(self, obj):
        count = obj.products_count
        return format_html(
            '<span style="color: {};">{}</span>',
            '#28a745' if count > 0 else '#dc3545',
            count
        )

    products_count.short_description = _("Mahsulotlar soni")


class ProductImageInline(TranslationTabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'sort_order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return _("Rasm yo'q")

    image_preview.short_description = _("Ko'rinish")


class ProductSpecificationInline(TranslationTabularInline):
    model = ProductSpecification
    extra = 1
    fields = ['name', 'value', 'sort_order']


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = [
        'name', 'category', 'price', 'old_price', 'discount_badge',
        'rating_display', 'views_count', 'reviews_count', 'is_active',
        'is_featured', 'main_image_preview'
    ]
    list_filter = [
        'category', 'is_active', 'is_featured',
        'created_at', 'price'
    ]
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_featured', 'price']
    readonly_fields = [
        'main_image_preview', 'views_count', 'rating',
        'reviews_count', 'discount_percentage', 'created_at', 'updated_at'
    ]
    inlines = [ProductImageInline, ProductSpecificationInline]

    fieldsets = (
        (_('Asosiy ma\'lumotlar'), {
            'fields': (
                'category', 'name', 'slug', 'short_description',
                'description', 'main_image', 'main_image_preview'
            )
        }),
        (_('Narx ma\'lumotlari'), {
            'fields': ('price', 'old_price', 'discount_percentage')
        }),
        (_('Sozlamalar'), {
            'fields': ('is_active', 'is_featured')
        }),
        (_('Statistika'), {
            'fields': ('views_count', 'rating', 'reviews_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px;" />',
                obj.main_image.url
            )
        return _("Rasm yo'q")

    main_image_preview.short_description = _("Asosiy rasm")

    def discount_badge(self, obj):
        discount = obj.discount_percentage
        if discount > 0:
            return format_html(
                '<span style="background: #dc3545; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">-{}%</span>',
                discount
            )
        return '-'

    discount_badge.short_description = _("Chegirma")

    def rating_display(self, obj):
        stars = '⭐' * int(obj.rating)
        return format_html(
            '<span title="{}/5">{} ({})</span>',
            obj.rating, stars, obj.rating
        )

    rating_display.short_description = _("Reyting")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')