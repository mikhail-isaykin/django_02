from django.views.generic import TemplateView, DetailView
from .models import Category, Product, Resume, Profile, Gallery, Photo
from django.contrib import messages
from django.shortcuts import render
from .forms import (
    FeedbackForm, ProfileForm, LoginForm,
    ContactForm, UsernameForm, PasswordForm,
    RegisterForm, FeedbackForm, UserRegisterForm,
    ArticleForm, ResumeForm, PhotoUploadForm,
    ContactFormset, OrderFormset, TaskFormset,
    StudentFormset, ProductFormset, RegistrationForm,
)
from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import login
User = get_user_model()


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


def order(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = order.product.price * order.quantity
            order.save()
            return redirect('products:order')
    return render(request, 'form.html', {'form': form})


def event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:event')
    return render(request, 'event.html', {'form': form})


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('products:register')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def article_view(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            print('Успех')
            print(
                f'{form.cleaned_data["title"]} - {form.cleaned_data["slug"]} - {form.cleaned_data["content"]}'
            )
            return redirect('products:article')
    return render(request, 'article.html', {'form': form})

def resume_view(request):
    form = ResumeForm()
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            resume = form.cleaned_data['resume']
            new_resume = Resume(username=username, resume=resume)
            try:
                new_resume.full_clean()
                new_resume.save()
                return redirect('products:resume')
            except ValidationError as error:
                form.add_error('resume', error.message_dict['resume'])
                print(type(error), error)
    return render(
        request,
        'resume.html',
        {'form': form}
    )

def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:
                form.full_clean()
                form.save()
                return redirect('products:profile')
            except ValidationError as error:
                form.add_error('avatar', error.message_dict['avatar'])
    return render(
        request,
        'profile_edit.html',
        {'form': form, 'user': request.user}
    )

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

def multi_upload(request):
    form = PhotoUploadForm()
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = Gallery.objects.create()
            images = form.cleaned_data['image']
            for image in images:
                Photo.objects.create(gallery=gallery, image=image)
            return redirect('products:gallery')
    return render(
        request,
        'products/gallery_upload.html',
        {'form': form}
    )

def formset_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password']
            }
            user = User.objects.create_user(**data)
            print(user)
            login(request, user)
            return redirect('products:formset')
    return render(
        request,
        'products/formset.html',
        {'form': form}
    )
