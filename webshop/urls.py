from django.urls import path
from . import views


urlpatterns = [
    #path('manufacturers/<int:manufacturer_id>/products/', views.ManufacturerProductsView.as_view(), name='manufacturer_products'),
    path('<str:sku>/availability/', views.UpdateProductAvailabilityView.as_view(), name='update_product'),
    path('about-us/', views.AboutUsView.as_view(), name='about_html'),
    path('', views.WelcomeHomeView.as_view(), name='welcome_home'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('product/<str:product_sku>/detail/', views.ProductDetailWithRelatedView.as_view(), name='product_detail'),
    path('manufacturers/', views.ManufacturerListView.as_view(), name='manufacturers_list'),
    path('old-home/', views.RedirectToHomeView.as_view(), name='old_home'),
    path('old-products-url/<str:old_sku>/', views.OldProductURLRedirectView.as_view(), name='redirect'),
    path('products/search/', views.ProductSearchView.as_view(), name='product_search'),
    path('legacy-search/', views.LegacySearchRedirectView.as_view(), name='search_redirect'),
    path('find-manufacturer/', views.ManufacturerLookupRedirectView.as_view(), name='find_manufacturer'),
    path('product-status/<str:product_sku>/', views.ProductAvailabilityRedirectView.as_view(), name='product_status'),
    path('product-unavailable/', views.ProductUnavailableView.as_view(), name='product_unavailable'),
    path('manufacturers/<int:pk>/', views.ManufacturerDetailView.as_view(), name='manufacturer_detail'),
    path('products/<str:product_sku>/', views.ProductDetailBySkuView.as_view(), name='product_detail_by_sku'),
    path('manufacturers/<int:pk>/products/', views.ManufacturerProductsDetailView.as_view(), name='manufacturers_all_products'),
    path('products/counted/<str:product_sku>/', views.ProductDetailWithViewCount.as_view(), name='views_count'),
    path('products/similar/<str:product_sku>/', views.ProductDetailWithSimilarPriceView.as_view(), name='similar_products'),
]
