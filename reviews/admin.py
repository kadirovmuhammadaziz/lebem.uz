from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from .models import Review, ContactMessage


@admin.register(Review)
class ReviewAdmin(TranslationAdmin):
    list_display = [
        'name', 'product', 'rating_display', 'phone',
        'is_active', 'created_at', 'comment_preview'
    ]
    list_filter = ['rating', 'is_active', 'created_at', 'product__category']
    search_fields = ['name', 'comment', 'phone', 'product__name']
    list_editable = ['is_active']
    readonly_fields = ['ip_address', 'created_at', 'updated_at']

    fieldsets = (
        (_('Foydalanuvchi ma\'lumotlari'), {
            'fields': ('name', 'phone', 'ip_address')
        }),
        (_('Sharh ma\'lumotlari'), {
            'fields': ('product', 'rating', 'comment')
        }),
        (_('Sozlamalar'), {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def rating_display(self, obj):
        stars = '⭐' * obj.rating
        color = '#28a745' if obj.rating >= 4 else '#ffc107' if obj.rating >= 3 else '#dc3545'
        return format_html(
            '<span style="color: {};" title="{}/5">{}</span>',
            color, obj.rating, stars
        )

    rating_display.short_description = _("Baho")

    def comment_preview(self, obj):
        if len(obj.comment) > 50:
            return obj.comment[:50] + '...'
        return obj.comment

    comment_preview.short_description = _("Izoh")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        # Update product ratings for activated reviews
        for review in queryset:
            review.update_product_rating()
        self.message_user(request, f'{updated} ta sharh faollashtirildi.')

    make_active.short_description = _("Tanlangan sharhlarni faollashtirish")

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        # Update product ratings after deactivation
        products = set(review.product for review in queryset)
        for product in products:
            # Recalculate rating for each affected product
            from django.db.models import Avg
            avg_rating = product.reviews.filter(is_active=True).aggregate(
                avg=Avg('rating')
            )['avg']
            product.rating = round(avg_rating, 2) if avg_rating else 0.00
            product.save(update_fields=['rating'])

        self.message_user(request, f'{updated} ta sharh o\'chirildi.')

    make_inactive.short_description = _("Tanlangan sharhlarni o'chirish")


@admin.register(ContactMessage)
class ContactMessageAdmin(TranslationAdmin):
    list_display = [
        'name', 'phone', 'subject_display', 'is_read',
        'created_at', 'message_preview'
    ]
    list_filter = ['subject', 'is_read', 'created_at']
    search_fields = ['name', 'phone', 'email', 'message']
    list_editable = ['is_read']
    readonly_fields = ['ip_address', 'created_at']

    fieldsets = (
        (_('Aloqa ma\'lumotlari'), {
            'fields': ('name', 'phone', 'email', 'ip_address')
        }),
        (_('Xabar ma\'lumotlari'), {
            'fields': ('subject', 'message')
        }),
        (_('Holat'), {
            'fields': ('is_read', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def subject_display(self, obj):
        colors = {
            'inquiry': '#17a2b8',
            'support': '#28a745',
            'complaint': '#dc3545',
            'suggestion': '#ffc107',
            'order': '#6f42c1'
        }
        color = colors.get(obj.subject, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_subject_display()
        )

    subject_display.short_description = _("Mavzu")

    def message_preview(self, obj):
        if len(obj.message) > 60:
            return obj.message[:60] + '...'
        return obj.message

    message_preview.short_description = _("Xabar")

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} ta xabar o\'qilgan deb belgilandi.')

    mark_as_read.short_description = _("O'qilgan deb belgilash")

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} ta xabar o\'qilmagan deb belgilandi.')

    mark_as_unread.short_description = _("O'qilmagan deb belgilash")