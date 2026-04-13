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
    FeedbackForm,
)
from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy


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


class FeedbackView(View):
    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:feedback')
        return render(request, 'registration.html', {'form': form})

    def get(self, request):
        form = FeedbackForm()
        return render(request, 'registration.html', {'form': form})


class FeedbackView(FormView):
    template_name = 'registration.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('products:feedback')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
