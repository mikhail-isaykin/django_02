from django.http import HttpResponse


def home_page(request):
    return HttpResponse('Добро пожаловать в мой блог!')


def greet_name(request, name):
    return HttpResponse(f'Привет, {name}')


def post_detail(request, post_id):
    return HttpResponse(f'Вы просматриваете пост с ID: {post_id}')
