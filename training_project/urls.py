from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views
from traning_app import views as traning_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('', blog_views.project_home, name='project_home'),
    path('api/v1/', include('blog.api_v1_urls')),
    path('api/v2/', include('blog.api_v2_urls')),
    path('products/', include('traning_app.urls')),
    path('top-products/', include('traning_app.urls')),
    path('api/', include('traning_app.urls')),
    path('cbv-home/', traning_views.HomePageCBV.as_view(), name='home_page')
]
