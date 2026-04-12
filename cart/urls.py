from django.urls import path
from .views import CartDetailView, add_to_cart, CartPurchaseView


app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='detail'),
    path('add/<slug:product_slug>/', add_to_cart, name='add_to_cart'),
    path('purchase/', CartPurchaseView.as_view(), name='purchase'),
]
