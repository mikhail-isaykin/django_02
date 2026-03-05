from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
from django.views.decorators.http import require_http_methods


def notes_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'notes': notes})


def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/detail.html', {'note': note})


def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():  # Валидация данных
            form.save()
            return redirect('notes_list')  # Редирект после сохранения
    else:
        form = NoteForm()
    return render(request, 'notes/form.html', {'form': form, 'title': 'Создать заметку'})


def note_edit(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_detail', note_id=note.id)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/form.html', {'form': form, 'title': 'Редактировать заметку'})


@require_http_methods(["GET", "POST"])
def note_delete(request, note_id):
    note = get_object_or_404(Note, pk=note_id)

    if request.method == 'POST':
        note.delete()
        return redirect('notes_list')

    return render(request, 'notes/confirm_delete.html', {'note': note})
