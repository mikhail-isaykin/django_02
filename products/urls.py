from django.urls import path
from .views import (
    HomePageView, registration, article_view,
    resume_view, profile_view, ProfileView,
    multi_upload, formset_view,
    )


app_name = 'products'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('registration/', registration, name='registration'),
    path('article/', article_view, name='article'),
    path('resume/', resume_view, name='resume'),
    path('profile/edit', profile_view, name='profile_edit'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('gallery/', multi_upload, name='gallery'),
    path('formset/', formset_view, name='formset'),
]
