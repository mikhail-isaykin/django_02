from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods



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


def conditional_redirect(request):
    target = request.GET.get('goto')

    if target == 'google':
        return HttpResponseRedirect("https://www.google.com")
    elif target == 'yandex':
        return HttpResponseRedirect("https://www.yandex.ru")
    else:
        return HttpResponse("Куда хотите перейти? Используйте ?goto=google или ?goto=yandex.")


@require_http_methods(["GET"])
def user_profile(request, user_id):
    users = {
        1: {"username": "admin", "role": "superuser", "active": True},
        2: {"username": "john_doe", "role": "editor", "active": False},
    }

    user = users.get(user_id)

    if user is None:
        return JsonResponse({"error": "Пользователь не найден."}, status=404)

    return JsonResponse({"status": "ok", "user": user})


@require_http_methods(["GET"])
def product_list(request):
    category = request.GET.get("category")

    products = [
        {"id": 1, "name": "Ноутбук", "category": "electronics", "price": 75000},
        {"id": 2, "name": "Кофеварка", "category": "appliances", "price": 4500},
        {"id": 3, "name": "Наушники", "category": "electronics", "price": 12000},
    ]

    if category:
        products = [p for p in products if p["category"] == category]

    return JsonResponse({"count": len(products), "products": products})


