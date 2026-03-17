from django.urls import path
from . import views


urlpatterns = [
    path('', views.api_v2_data, name='v2_data')
]
