from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
import json


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


@require_http_methods(["POST"])
def login_view(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Невалидный JSON."}, status=400)

    username = body.get("username", "").strip()
    password = body.get("password", "").strip()

    if not username or not password:
        return JsonResponse({"error": "Укажите username и password."}, status=422)

    if username == "admin" and password == "1234":
        return JsonResponse({"status": "ok", "token": "abc123xyz"})

    return JsonResponse({"error": "Неверные учётные данные."}, status=401)


@require_http_methods(["GET"])
def product_search(request):
    products = [
        {"id": 1, "name": "Ноутбук",   "category": "electronics", "price": 75000, "rating": 4.8},
        {"id": 2, "name": "Кофеварка", "category": "appliances",  "price": 4500,  "rating": 3.9},
        {"id": 3, "name": "Наушники",  "category": "electronics", "price": 12000, "rating": 4.5},
        {"id": 4, "name": "Телефон",   "category": "electronics", "price": 55000, "rating": 4.2},
        {"id": 5, "name": "Блендер",   "category": "appliances",  "price": 3200,  "rating": 4.1},
    ]

    query    = request.GET.get("q", "").strip().lower()
    category = request.GET.get("category", "").strip()
    sort_by  = request.GET.get("sort", "id")
    order    = request.GET.get("order", "asc")
    page     = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 2))

    ALLOWED_SORT_FIELDS = {"id", "price", "rating"}
    if sort_by not in ALLOWED_SORT_FIELDS:
        return JsonResponse({"error": f"Недопустимое поле сортировки. Доступно: {', '.join(ALLOWED_SORT_FIELDS)}."}, status=400)

    if query:
        products = [p for p in products if query in p["name"].lower()]
    if category:
        products = [p for p in products if p["category"] == category]

    products = sorted(products, key=lambda p: p[sort_by], reverse=(order == "desc"))

    total      = len(products)
    start      = (page - 1) * per_page
    products   = products[start:start + per_page]

    return JsonResponse({
        "total":    total,
        "page":     page,
        "per_page": per_page,
        "pages":    -(-total // per_page),  # ceil без math
        "results":  products,
    })

@require_http_methods(["POST"])
def bulk_action(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Невалидный JSON."}, status=400)

    action  = body.get("action", "").strip()
    ids     = body.get("ids", [])

    ALLOWED_ACTIONS = {"delete", "archive", "publish"}

    if action not in ALLOWED_ACTIONS:
        return JsonResponse({"error": f"Недопустимое действие. Доступно: {', '.join(ALLOWED_ACTIONS)}."}, status=400)

    if not isinstance(ids, list) or not ids:
        return JsonResponse({"error": "ids должен быть непустым списком."}, status=422)

    if not all(isinstance(i, int) for i in ids):
        return JsonResponse({"error": "Все элементы ids должны быть целыми числами."}, status=422)

    ids = list(set(ids))  # дедупликация

    return JsonResponse({
        "status":   "ok",
        "action":   action,
        "affected": len(ids),
        "ids":      ids,
    })


@require_http_methods(["GET"])
def activity_feed(request):
    events = [
        {"id": 1, "user": "admin",    "action": "created_post",   "target": "Пост #12", "timestamp": "2024-03-01T10:00:00"},
        {"id": 2, "user": "john_doe", "action": "commented",      "target": "Пост #12", "timestamp": "2024-03-01T10:15:00"},
        {"id": 3, "user": "admin",    "action": "deleted_comment", "target": "Комментарий #7", "timestamp": "2024-03-01T11:00:00"},
        {"id": 4, "user": "john_doe", "action": "published_post",  "target": "Пост #13", "timestamp": "2024-03-02T09:30:00"},
        {"id": 5, "user": "admin",    "action": "created_post",   "target": "Пост #14", "timestamp": "2024-03-02T14:00:00"},
        {"id": 6, "user": "john_doe", "action": "commented",      "target": "Пост #14", "timestamp": "2024-03-03T08:45:00"},
    ]

    user        = request.GET.get("user", "").strip()
    action      = request.GET.get("action", "").strip()
    date_from   = request.GET.get("from", "").strip()
    date_to     = request.GET.get("to", "").strip()
    limit       = request.GET.get("limit", 10)

    try:
        limit = max(1, min(int(limit), 100))
    except ValueError:
        return JsonResponse({"error": "limit должен быть числом."}, status=400)

    if user:
        events = [e for e in events if e["user"] == user]
    if action:
        events = [e for e in events if e["action"] == action]
    if date_from:
        events = [e for e in events if e["timestamp"] >= date_from]
    if date_to:
        events = [e for e in events if e["timestamp"] <= date_to]

    events = events[:limit]

    return JsonResponse({
        "count":  len(events),
        "limit":  limit,
        "events": events,
    })

