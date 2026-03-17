from django.http import HttpResponse


def home_page(request):
    return HttpResponse('Добро пожаловать в мой блог!')


def greet_name(request, name):
    return HttpResponse(f'Привет, {name}')


def post_detail(request, post_id):
    return HttpResponse(f'Вы просматриваете пост с ID: {post_id}')


def archive_by_month(request, year, month):
    return HttpResponse(f'Вы просматриваете архив за {month}/{year}.')


def project_home(request):
    return HttpResponse('Добро пожаловать на главную страницу проекта!')


def greet_optional(request, name='незнакомец'):
    return HttpResponse(f'Привет, {name}!')


def api_v1_data(request):
    return HttpResponse('Это API v1')


def api_v2_data(request):
    return HttpResponse('Это API v2')


def product_slug(request, slug):
    return HttpResponse(f'Вы просматриваете продукт со слагом: {slug}')


def new_user_profile(request, user_id):
    return HttpResponse(f'Это новый профиль пользователя ID: {user_id}')