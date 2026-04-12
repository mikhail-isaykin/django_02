from django.urls import path
from .views import HomePageView, registration


app_name = 'products'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('registration/', registration, name='registration'),
]
