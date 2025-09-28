from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/reviews/', include('reviews.urls')),
]

# Internationalization URLs
urlpatterns += i18n_patterns(
    path('rosetta/', include('rosetta.urls')),
    prefix_default_language=False,
)

# Media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin panel customization
admin.site.site_header = "Lebem.uz Admin Panel"
admin.site.site_title = "Lebem.uz"
admin.site.index_title = "Mebel do'koni boshqaruvi"
