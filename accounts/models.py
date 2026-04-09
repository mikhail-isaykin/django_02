from django.db import models
from django.conf import settings
import uuid


class BankAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bank_account'
    )
    account_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )


    def __str__(self):
        return f"{self.user.username} - {self.account_number} ({self.balance} ₽)"


    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)
    
    
    def generate_account_number(self):
        # Пример: 2202 + уникальные цифры
        return "2202" + str(uuid.uuid4().int)[:12]  # 16 цифр
