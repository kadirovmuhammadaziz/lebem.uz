# apps/products/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview', 'products_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px;"/>',
                obj.image.url
            )
        return "Rasm yo'q"

    image_preview.short_description = 'Rasm'

    def products_count(self, obj):
        return obj.products.count()

    products_count.short_description = 'Mahsulotlar soni'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'image_preview', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_featured', 'is_active', 'price')
    inlines = [ProductImageInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px;"/>',
                obj.image.url
            )
        return "Rasm yo'q"

    image_preview.short_description = 'Rasm'

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Narx va rasmlar', {
            'fields': ('price', 'image')
        }),
        ('Sozlamalar', {
            'fields': ('is_featured', 'is_active')
        }),
    )
