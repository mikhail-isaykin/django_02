from django.http import HttpResponse


def home_page(request):
    return HttpResponse("Добро пожаловать в мой блог!")
