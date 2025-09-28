from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nomi"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    description = models.TextField(blank=True, verbose_name=_("Tavsif"))
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        verbose_name=_("Rasm")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Tartiblash")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("O'zgartirilgan"))

    class Meta:
        verbose_name = _("Kategoriya")
        verbose_name_plural = _("Kategoriyalar")
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    @property
    def products_count(self):
        return self.products.filter(is_active=True).count()


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_("Kategoriya")
    )
    name = models.CharField(max_length=200, verbose_name=_("Nomi"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    description = models.TextField(verbose_name=_("Tavsif"))
    short_description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Qisqa tavsif")
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Narx")
    )
    old_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("Eski narx")
    )
    main_image = models.ImageField(
        upload_to='products/',
        default='products/default.jpg',   # agar asosiy rasm tanlanmasa
        verbose_name=_("Asosiy rasm")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))
    is_featured = models.BooleanField(default=False, verbose_name=_("Tanlanganlar"))
    views_count = models.PositiveIntegerField(default=0, verbose_name=_("Ko'rishlar soni"))
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name=_("Reyting")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("O'zgartirilgan"))

    class Meta:
        verbose_name = _("Mahsulot")
        verbose_name_plural = _("Mahsulotlar")
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return round(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    @property
    def reviews_count(self):
        return self.reviews.filter(is_active=True).count()

    @property
    def gallery_images(self):
        """Asosiy rasmdan tashqari qo‘shimcha rasmlar"""
        return self.images.all()

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            self.slug = slugify(self.name) + '-' + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_("Mahsulot")
    )
    image = models.ImageField(
        upload_to='products/gallery/',
        verbose_name=_("Rasm")
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Alt matn")
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Tartiblash")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan"))

    class Meta:
        verbose_name = _("Mahsulot rasmi")
        verbose_name_plural = _("Mahsulot rasmlari")
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f"{self.product.name} - Rasm {self.id}"



class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='specifications',
        verbose_name=_("Mahsulot")
    )
    name = models.CharField(max_length=100, verbose_name=_("Xususiyat nomi"))
    value = models.CharField(max_length=200, verbose_name=_("Qiymati"))
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Tartiblash")
    )

    class Meta:
        verbose_name = _("Mahsulot xususiyati")
        verbose_name_plural = _("Mahsulot xususiyatlari")
        ordering = ['sort_order', 'name']
        unique_together = [['product', 'name']]

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"