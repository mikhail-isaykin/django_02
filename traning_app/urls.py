from django.urls import path
from . import views

urlpatterns = [
    path('category/<str:category_name>/', views.product_list_by_category, name='product_list_by_category'),
    path('', views.top_products, name='top_products'),
    path('products/<int:pk>/', views.product_detail_api, name='product_detail_api'),
    path('products/<int:product_id>/update-price/', views.update_price, name='update_price'),
]
