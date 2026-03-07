from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("",                  views.CatalogView.as_view(),       name="index"),
    path("<slug:slug>/",      views.ProductDetailView.as_view(), name="product_detail"),
    # path("newsletter/signup/", views.newsletter_signup,          name="newsletter_signup"),
]
