from django.urls import path
from . import views


urlpatterns = [
    path('', views.notes_list, name='notes_list'),
    path('<int:note_id>/', views.note_detail, name='note_detail'),
    path('create/', views.note_create, name='note_create'),
    path('<int:note_id>/edit/', views.note_edit, name='note_edit'),
    path('<int:note_id>/delete/', views.note_delete, name='note_delete'),
]
