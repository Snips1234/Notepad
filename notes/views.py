
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, NoteImage
from .forms import NoteForm

def home(request):
    notes = Note.objects.order_by('-created_at')
    return render(request, 'notes/home.html', {'notes': notes})


def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        files = request.FILES.getlist('note_images')
        if form.is_valid():
            note = form.save()
            for f in files:
                NoteImage.objects.create(note=note, image=f)
            return JsonResponse({'success': True})
    else:
        form = NoteForm()
    return render(request, 'notes/note_form_partial.html', {'form': form, 'action': 'Add'})

def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            note = form.save()

            new_images = request.FILES.getlist('new_images')
            for img in new_images:
                NoteImage.objects.create(note=note, image=img)

            deleted_images = request.POST.get('deleted_images', '')
            if deleted_images:
                image_ids = deleted_images.split(',')
                note.images.filter(id__in=image_ids).delete()

            return JsonResponse({'success': True})
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/edit_form_partial.html', {'form': form, 'action': 'Edit', 'note': note})


def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return JsonResponse({'success': True})
    return render(request, 'notes/delete_form_partial.html', {'note': note})

def delete_image(request, image_id):
    if request.method == 'POST':
        try:
            image = NoteImage.objects.get(id=image_id)
            image.delete()
            return JsonResponse({'success': True})
        except NoteImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
