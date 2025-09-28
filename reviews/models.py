from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from products.models import Product


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_("Mahsulot")
    )
    name = models.CharField(max_length=100, verbose_name=_("Ism"))
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+998[0-9]{9}$',
                message=_("Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak")
            )
        ],
        verbose_name=_("Telefon raqam")
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,   # 🔑 shu qo‘shildi
        verbose_name=_("Baho (1-5)")
    )
    comment = models.TextField(verbose_name=_("Izoh"))
    is_active = models.BooleanField(default=False, verbose_name=_("Faol"))
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name=_("IP manzil")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("O'zgartirilgan"))

    class Meta:
        verbose_name = _("Sharh")
        verbose_name_plural = _("Sharhlar")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'is_active']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.name} - {self.product.name} ({self.rating}⭐)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_active:  # faqat faol sharhlar hisobga olinadi
            self.update_product_rating()

    def update_product_rating(self):
        """Update the product's average rating"""
        from django.db.models import Avg
        avg_rating = self.product.reviews.filter(is_active=True).aggregate(
            avg=Avg('rating')
        )['avg']

        if avg_rating:
            self.product.rating = round(avg_rating, 2)
            self.product.save(update_fields=['rating'])


class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('inquiry', _('Umumiy so\'rov')),
        ('support', _('Texnik yordam')),
        ('complaint', _('Shikoyat')),
        ('suggestion', _('Taklif')),
        ('order', _('Buyurtma haqida')),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Ism"))
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+998[0-9]{9}$',
                message=_("Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak")
            )
        ],
        verbose_name=_("Telefon raqam")
    )
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    subject = models.CharField(
        max_length=20,
        choices=SUBJECT_CHOICES,
        default='inquiry',
        verbose_name=_("Mavzu")
    )
    message = models.TextField(verbose_name=_("Xabar"))
    is_read = models.BooleanField(default=False, verbose_name=_("O'qilgan"))
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name=_("IP manzil")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan"))

    class Meta:
        verbose_name = _("Aloqa xabari")
        verbose_name_plural = _("Aloqa xabarlari")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"