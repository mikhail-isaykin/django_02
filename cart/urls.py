from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("",              views.CartDetailView.as_view(),  name="detail"),
    path("summary/",      views.CartSummaryView.as_view(), name="summary"),
    path("add/<int:product_id>/", views.CartAddView.as_view(),    name="add"),
    path("update/",       views.CartUpdateView.as_view(), name="update"),
    path("remove/",       views.CartRemoveView.as_view(), name="remove"),
]
