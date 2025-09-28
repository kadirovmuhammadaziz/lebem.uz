from django.db import models
from django.core.validators import RegexValidator
from products.models import Product


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Mahsulot")
    name = models.CharField(max_length=100, verbose_name="Ism")
    phone = models.CharField(validators=[], max_length=15, verbose_name="Telefon raqam")
    comment = models.TextField(verbose_name="Izoh")
    is_processed = models.BooleanField(default=False, verbose_name="Ko'rib chiqilgan")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.product.name}"
