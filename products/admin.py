from django.contrib import admin
from .models import (
    Article,
    Profile,
    Author,
    Book,
    Product,
    Course,
    BlogPost,
    Customer,
    Order,
    OrderItem,
    Job,
    Ad,
)
from django import forms
from django.utils.text import slugify
from itertools import count


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    readonly_fields = ['slug']
    list_filter = ['author']
    search_fields = ['title']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'website', 'location']
    fieldsets = [
        ('Личная информация', {'fields': ['user', 'bio']}),
        ('Дополнительно', {'fields': ['website', 'location']}),
    ]


#
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    list_filter = ['published_date']
    search_fields = ['title', 'author__name']
    ordering = ['-published_date']
    readonly_fields = ['created_at']
    fields = ['title', 'description', 'author', 'published_date']


class BookTabularInline(admin.TabularInline):
    model = Book
    fields = [
        'author',
        'title',
        'description',
        'published_date',
        'internal_notes',
        'created_at',
    ]
    readonly_fields = ['created_at']
    extra = 1
    can_delete = True


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Основная информация', {'fields': ['name', 'birth_date']}),
        ('Контакт', {'fields': ['email']}),
    ]
    inlines = [BookTabularInline]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price', 'in_stock']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не може быть отрицаельной')
        return price

    def clean_slug(self):
        pk = {'pk': self.instance.pk}
        slug = self.cleaned_data['slug']
        if not slug or Product.objects.filter(slug=slug).exclude(**pk).exists():
            counter = count(1)
            slug = slugify(self.cleaned_data['name'])
            slug_with_suffix = slug  # изначально без суффикса
            while Product.objects.filter(slug=slug_with_suffix).exclude(**pk).exists():
                slug_with_suffix = slug + '-' + str(next(counter))
            slug = slug_with_suffix
        return slug


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    fields = ['name', 'slug', 'description', 'price', 'in_stock', 'created_at']
    readonly_fields = ['created_at']
    prepopulated_fields = prepopulated_fields = {'slug': ['name']}
    list_display = ['name', 'price', 'in_stock', 'created_at']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        discount_price = cleaned_data.get('discount_price')
        price = cleaned_data.get('price')
        if discount_price and discount_price > price:
            raise forms.ValidationError('Скидка должна быть <= цена')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    readonly_fields = ['created_at']
    list_display = ['title', 'price', 'discount_price', 'is_active']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at']

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = BlogPostAdmin.generate_unique_slug(obj.title, obj.pk)
        super().save_model(request, obj, form, change)

    @staticmethod
    def generate_unique_slug(title, pk):
        counter = count(1)
        slug = slugify(title)
        slug_with_suffix = slug
        while BlogPost.objects.filter(slug=slug_with_suffix).exclude(pk=pk).exists():
            slug_with_suffix = slug + '-' + str(next(counter))
        return slug_with_suffix


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_display = ['first_name', 'last_name', 'email', 'created_at']
    search_fields = ['first_name', 'email']
    readonly_fields = ['created_at']


#
class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Основная информация', {'fields': ['customer', 'status']}),
        ('Системные данные', {'fields': ['created_at', 'updated_at']}),
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    inlines = [OrderItemTabularInline]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']
    list_display = ['title', 'status', 'created_at']
    list_editable = ['status']


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at']
    readonly_fields = ['created_at']
    prepopulated_fields = {'slug': ['title']}
    save_as = True
    actions = ['make_published']

    @admin.action(description='Опубликовать выбранные')
    def make_published(self, request, queryset):
        updated = queryset.filter(status='draft').update(status='published')
        self.message_user(request, f'Опубликовано {updated} объявлений.')

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = AdAdmin.generate_unique_slug(obj.title, obj.pk)
        super().save_model(request, obj, form, change)

    @staticmethod
    def generate_unique_slug(title, pk):
        counter = count(1)
        slug = slugify(title)
        slug_with_suffix = slug
        while Ad.objects.filter(slug=slug_with_suffix).exclude(pk=pk).exists():
            slug_with_suffix = slug + '-' + str(next(counter))
        return slug_with_suffix
