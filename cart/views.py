from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
@require_POST
def add_to_cart(request, product_slug):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    product = get_object_or_404(Product, slug=product_slug)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    redirect_page = request.META.get('HTTP_REFERER', reverse('home_page'))
    return redirect(redirect_page)


class CartDetailView(LoginRequiredMixin, ListView):
    template_name = 'cart_detail.html'
    context_object_name = 'cart_items'


    def get_queryset(self):
        self.cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return self.cart.items.all()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context
