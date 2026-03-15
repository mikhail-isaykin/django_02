from django.db.models import F, Window, Sum, Count, ExpressionWrapper, DecimalField
from django.db.models.functions import Rank, DenseRank
from traning_app.models import Product, Customer, Order


Product.objects.annotate(
    final_price=ExpressionWrapper(
        F('price') * (1 - F('discount') / Decimal('100')),
        output_field=DecimalField(max_digits=8, decimal_places=2)
    )
).values('name', 'final_price')[:5]


Product.objects.annotate(
    rank=Window(
        expression=DenseRank(),
        order_by=F('rating').desc()
    )
).values('name', 'rating', 'rank')[:5]


Customer.objects.annotate(orders_count=Count("orders")).filter(orders_count__gt=0).annotate(total_sum=ExpressionWrapper(
    Sum("orders__total"),
    output_field=DecimalField()),
    rank=Window(
        expression=Rank(),
        order_by=F("total_sum").desc()
    )
).values("name", "total_sum", "rank")[:3]
