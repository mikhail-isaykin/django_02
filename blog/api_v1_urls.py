from django.urls import path
from . import views


urlpatterns = [
    path('', views.api_v1_data, name='v1_data')
]
