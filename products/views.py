from django.views.generic import TemplateView, DetailView
from .models import Category, Product
from django.contrib import messages
from django.shortcuts import render
from .forms import (
    FeedbackForm,
    ProfileForm,
    LoginForm,
    ContactForm,
    UsernameForm,
    PasswordForm,
    RegisterForm,
)
from django.shortcuts import redirect


class HomePageView(TemplateView):
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(is_active=True)
        selected_category = self.request.GET.get('category')
        products = Product.objects.filter(
            category__slug=selected_category, is_active=True
        )
        context['categories'] = categories
        context['selected_category'] = selected_category
        context['products'] = products
        return context


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('Форма успешно отправлена!')
            # print(f'Имя: {form.cleaned_data["name"]}')
            # print(f'Email: {form.cleaned_data["email"]}')
            # print(f'Сообщение: {form.cleaned_data["message"]}')
            return redirect('products:registration')
    else:
        form = RegisterForm()
    return render(request, 'products/registration.html', {'form': form})
