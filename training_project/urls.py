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
    path('cbv-home/', traning_views.HomePageCBV.as_view(), name='home_page'),
    path('contact/cbv/', traning_views.ContactFormCBV.as_view(), name='contact_page'),
    path('products/cbv/<int:product_id>/', traning_views.ProductDetailCBV.as_view(), name='product_detail'),
    path('api/status/cbv/', traning_views.SystemInfoCBV.as_view(), name='system_info'),
    path('secure-page/cbv/', traning_views.AuthCheckCBV.as_view(), name='auth_check'),
    path('products/<int:product_id>/rating/<int:user_rating>/', traning_views.ProductRatingView.as_view(), name='get_only'),
    path('products/<int:product_id>/submit-rating/', traning_views.ProductRatingView.as_view(), name='post_only'),
    path('webshop/', include('webshop.urls')),
    path('api/products/', include('webshop.urls')),
]
