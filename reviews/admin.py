from django.contrib import admin
from django.utils.html import format_html
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'phone', 'is_processed', 'created_at')
    list_filter = ('is_processed', 'created_at', 'product__category')
    search_fields = ('name', 'phone', 'comment', 'product__name')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Mijoz ma\'lumotlari', {
            'fields': ('name', 'phone')
        }),
        ('Mahsulot va izoh', {
            'fields': ('product', 'comment')
        }),
        ('Holat', {
            'fields': ('is_processed', 'created_at')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')

    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        updated = queryset.update(is_processed=True)
        self.message_user(request, f'{updated} ta izoh ko\'rib chiqilgan deb belgilandi.')

    mark_as_processed.short_description = 'Ko\'rib chiqilgan deb belgilash'
