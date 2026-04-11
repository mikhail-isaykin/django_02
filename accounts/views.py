from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import BankAccount
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.shortcuts import redirect


@login_required
def bank_account_view(request):
    bank_account = get_object_or_404(BankAccount, user=request.user)
    return render(
        request,
        'accounts/bank_account.html',
        {'bank_account': bank_account}
    )


class DepositAccountView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs): 
        self.bank_account = get_object_or_404(BankAccount, user=request.user)
        return super().dispatch(request, *args, **kwargs)
    

    def post(self, request):
        try:
            amount = Decimal(request.POST.get('amount'))
            if amount <= 0:
                raise InvalidOperation
            self.bank_account.balance += amount
            self.bank_account.save()
            return redirect('bank_account')
        except InvalidOperation:
            messages.error(request, 'Введите корректную сумму больше нуля.')
            return redirect('deposit_account')



    def get(self, request):
        return render(
            request,
            'accounts/deposit_account.html',
            {'bank_account': self.bank_account}
        )
