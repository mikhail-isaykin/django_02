from django import forms
from .models import Product, Category, Order, Customer


class ProductFilterForm(forms.Form):
    SORT_CHOICES = [
        ('price_asc',    'Цена: по возрастанию'),
        ('price_desc',   'Цена: по убыванию'),
        ('rating_desc',  'Рейтинг: высокий'),
        ('created_desc', 'Сначала новые'),
    ]

    search    = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию...'}),
    )
    category  = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='Все категории',
    )
    price_min = forms.DecimalField(
        required=False,
        min_value=0,
        max_digits=6,
        decimal_places=2,
        label='Цена от',
    )
    price_max = forms.DecimalField(
        required=False,
        min_value=0,
        max_digits=6,
        decimal_places=2,
        label='Цена до',
    )
    rating_min = forms.FloatField(
        required=False,
        min_value=0,
        max_value=5,
        label='Рейтинг от',
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label='Сортировка',
    )

    def clean(self):
        cleaned = super().clean()
        price_min = cleaned.get('price_min')
        price_max = cleaned.get('price_max')

        if price_min and price_max and price_min > price_max:
            raise forms.ValidationError('Минимальная цена не может быть больше максимальной.')

        return cleaned


class OrderCreateForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(orders__is_active=True).distinct(),
        empty_label='Выберите покупателя',
        label='Покупатель',
    )
    total = forms.DecimalField(
        min_value=0,
        max_digits=8,
        decimal_places=2,
        label='Сумма заказа',
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label='Активный заказ',
    )

    class Meta:
        model  = Order
        fields = ['customer', 'total', 'is_active']

    def clean_total(self):
        total = self.cleaned_data.get('total')

        if total <= 0:
            raise forms.ValidationError('Сумма заказа должна быть больше нуля.')

        if total > 999999.99:
            raise forms.ValidationError('Сумма заказа превышает допустимый лимит.')

        return total

    def clean_customer(self):
        customer = self.cleaned_data.get('customer')

        if customer and customer.age < 18:
            raise forms.ValidationError('Заказ нельзя оформить на покупателя младше 18 лет.')

        return customer

