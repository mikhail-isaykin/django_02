from django.urls import path
from . import views

urlpatterns = [
    path('category/<str:category_name>/', views.product_list_by_category, name='product-list-by-category'),
    path('', views.top_products, name='top-products'),
]
