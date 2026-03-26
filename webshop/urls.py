from django.urls import path
from . import views


urlpatterns = [
    path('manufacturers/<int:manufacturer_id>/products/', views.ManufacturerProductsView.as_view(), name='manufacturer_products')
]
