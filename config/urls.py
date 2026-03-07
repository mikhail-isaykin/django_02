from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/",    admin.site.urls),
    path("",          include("catalog.urls",  namespace="catalog")),
    path("cart/",     include("cart.urls",     namespace="cart")),
    # path("orders/",   include("orders.urls",   namespace="orders")),
    # path("payments/", include("payments.urls", namespace="payments")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
