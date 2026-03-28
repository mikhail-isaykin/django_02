from django.urls import path
from . import views


urlpatterns = [
    path('manufacturers/<int:manufacturer_id>/products/', views.ManufacturerProductsView.as_view(), name='manufacturer_products'),
    path('<str:sku>/availability/', views.UpdateProductAvailabilityView.as_view(), name='update_product'),
    path('about-us/', views.AboutUsView.as_view(), name='about_html'),
    path('', views.WelcomeHomeView.as_view(), name='welcome_home'),
    path('faq/', views.FAQView.as_view(), name='faq'),
]
