from django.urls import path, re_path
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('greet/<str:name>/', views.greet_name, name='greet_name'),
    path('posts/<int:post_id>', views.post_detail, name='post_detail'),
    path('archive/<int:year>/<int:month>/', views.archive_by_month, name='archive_by_month'),
    path('greet/', views.greet_optional, name='greet_optional'),
    path('greet/<str:name>/', views.greet_optional, name='greet_optional_name'),
    re_path(r'^products/(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$', views.product_slug, name='product_slug'),
    path('users/<int:user_id>/profile/', views.new_user_profile, name='new_user_profile'),
    path('old-profiles/user/<int:user_id>/', RedirectView.as_view(permanent=True, pattern_name='new_user_profile'), name='old_user_profile_redirect'),
]
