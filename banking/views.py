from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import BankAccount
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.shortcuts import redirect
from django.db import transaction


@login_required
def bank_account_view(request):
    bank_account = get_object_or_404(BankAccount, user=request.user)
    return render(
        request,
        'accounts/bank_account.html',
        {'bank_account': bank_account}
    )


class DepositAccountView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            amount = Decimal(request.POST.get('amount'))
            if amount <= 0:
                raise InvalidOperation
            with transaction.atomic():
                bank_account = BankAccount.objects.select_for_update().get(user=request.user)
                bank_account.balance += amount
                bank_account.save()
            return redirect('bank_account')
        except InvalidOperation:
            messages.error(request, 'Введите корректную сумму больше нуля.')
            return redirect('deposit_account')



    def get(self, request):
        bank_account = get_object_or_404(BankAccount, user=request.user)
        return render(
            request,
            'accounts/deposit_account.html',
            {'bank_account': bank_account}
        )


class TransferMoneyView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            amount = Decimal(request.POST.get('amount'))
            if amount <= 0:
                raise InvalidOperation
        except InvalidOperation as error:
            messages.error(request, error)
            return redirect(?)
        recipient_username = request.POST.get('recipient_username')
        recipient_account = request.POST.get('recipient_account')
        if not recipient_username and not recipient_account:
            messages.error(request, 'Укажите получателя или банковский счет')
            return redirect()
        filters = {}
        if recipient_username:
            filters['user__username'] = recipient_username
        if recipient_account:
            filters['account_number'] = recipient_account

        try:
            with transaction.atomic():
                sender_bank_account = get_object_or_404(BankAccount.objects.select_for_update(), user=request.user) # отправитель
                if sender_bank_account.balance < amount:
                    messages.error(request, 'Недостаточно средств, пополните баланс')
                    return redirect()
                recipient_bank_account = get_object_or_404(BankAccount.objects.select_for_update(), **filters) # получатель
                sender_bank_account.balance -= amount
                sender_bank_account.save()
                recipient_bank_account.balance += amount
                recipient_bank_account.save()
                messages.success(request, ...)
                return redirect(...)
        except Exception as error:
            messages.error(request, error)
            return redirect(....)
        

    def get(self, request):
        return render(
            request,
            'accounts/transfer.html'
        )
