from django.db.models import F, Window, Sum, Count, ExpressionWrapper, DecimalField
from django.db.models.functions import Rank
from traning_app.models import Product


Product.objects.annotate(
    final_price=ExpressionWrapper(
        F('price') * (1 - F('discount') / Decimal('100')),
        output_field=DecimalField(max_digits=8, decimal_places=2)
    )
).values('name', 'final_price')[:5]
