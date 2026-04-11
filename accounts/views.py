from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import BankAccount
from django.shortcuts import get_object_or_404


@login_required
def bank_account_view(request):
    bank_account = get_object_or_404(BankAccount, user=request.user)
    return render(
        request,
        'accounts/bank_account.html',
        {'bank_account': bank_account}
    )


@login_required
def deposit_account_view(request):
    bank_account = get_object_or_404(BankAccount, user=request.user)
    return render(
        request,
        'accounts/deposit_account.html',
        {'bank_account': bank_account}
    )
