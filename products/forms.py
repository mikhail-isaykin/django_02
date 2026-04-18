from django import forms
from .models import Feedback, Resume, Profile, Photo
from datetime import date as dt
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from re import fullmatch
from django.forms import formset_factory


class FeedbackForm(forms.Form):
    name = forms.CharField(label='Имя пользователя', help_text='Только буквы и цифры')
    email = forms.EmailField(label='Ваш email')
    message = forms.CharField(label='Сообщение', help_text='Минимум 10 символов')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError('Email должен оканчиваться на @gmail.com')
        return email

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise forms.ValidationError('Cообщение не может быть короче 10 символов')
        return message


"""class ProfileForm(forms.Form):
    city = forms.CharField(label='Город', initial='Москва')"""


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Введите логин'})
    )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    remember_me = forms.BooleanField(
        label='Запомнить меня', widget=forms.CheckboxInput()
    )


'''class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема')
    email = forms.EmailField(label='Ваш email')
    message = forms.CharField(label='Сообщение')'''


class UsernameForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')

    def clean_username(self):
        username = self.cleaned_data['username']
        if '@' in username:
            raise forms.ValidationError(
                "Имя пользователя не должно содержать символ '@'"
            )
        return username


class PasswordForm(forms.Form):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        label='Подтвердите пароль', widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Пароли не совпадают')


class RegisterForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        label='Подтвердите пароль', widget=forms.PasswordInput()
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isalnum():
            raise forms.ValidationError(
                'Имя пользователя должно содержать только буквы и цифры'
            )
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Пароли не совпадают')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']


"""class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product', 'quantity']"""


"""class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date']

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < dt.today():
            raise forms.ValidationError('Дата не может быть в прошлом')
        return date"""


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Введите ваш email'}),
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value in self.fields.values():
            value.widget.attrs['class'] = 'form-control'

    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    email = forms.EmailField(
        max_length=30, widget=forms.EmailInput(attrs={'placeholder': 'Введите email'})
    )


class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].validators.append(self.validate_no_spaces)

    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

    @staticmethod
    def validate_no_spaces(value):
        if ' ' in value:
            raise ValidationError('Имя пользователя не должно содержать пробелов')


class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError('Email должен заканчиваться на @gmail.com')
        return email


class ArticleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].validators.append(type(self).is_slug)

    title = forms.CharField()
    slug = forms.CharField()
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 10:
            raise forms.ValidationError(
                'Заголовок должен содержать не менее 10 символов'
            )
        return title

    @staticmethod
    def is_slug(value):
        if not fullmatch(r'[a-z_]+', value):
            raise ValidationError('Slug может содержать только [a-z_]')


class ResumeForm(forms.Form):
    username = forms.CharField(max_length=100)
    resume = forms.FileField()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        label = {'avatar': 'Аватар'}


class PhotoUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'] = self.MultiplePhotoField(widget=self.MultiplePhotoInput())

    class MultiplePhotoInput(forms.ClearableFileInput):
        allow_multiple_selected = True

    class MultiplePhotoField(forms.ImageField):
        def clean(self, data, initial=None):
            if isinstance(data, (list, tuple)):
                return [super().clean(d, initial) for d in data]
            return [super().clean(data, initial)]

    class Meta:
        model = Photo
        fields = ['image']
        labels = {'image': 'Выберите фото'}


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=50)
    email = forms.EmailField(label='Email')


ContactFormset = formset_factory(ContactForm, min_num=2, extra=0)


class OrderForm(forms.Form):
    product_name = forms.CharField(label='Название продукта')
    quantity = forms.IntegerField(min_value=0)


OrderFormset = formset_factory(OrderForm, extra=3)
