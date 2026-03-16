from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('greet/<str:name>/', views.greet_name, name='greet_name'),
    path('posts/<int:post_id>', views.post_detail, name='post_detail'),
]
