from django.urls import path
from .views import bank_account_view, DepositAccountView, TransferMoneyView


app_name = 'banking'

urlpatterns = [
    path('', bank_account_view, name='bank'),
    path('add_deposit/', DepositAccountView.as_view(), name='add_deposit'),
    path('transfer/', TransferMoneyView.as_view(), name='transfer'),
]
