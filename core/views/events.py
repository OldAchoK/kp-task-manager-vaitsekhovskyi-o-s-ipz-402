from django.shortcuts import redirect
from django.contrib import messages as django_messages
from django.http import JsonResponse
from core.models import Event, EventHandler, Client


def create_event(request):
    if request.method == 'POST':
        try:
            evt = Event.objects.create(
                theme=request.POST.get('theme'),
                description=request.POST.get('description'),
                priority=request.POST.get('priority'),
                date=request.POST.get('date'),
                duration=request.POST.get('duration'),
                link=request.POST.get('link', ''),
                author_id=request.session.get('user_id')
            )

            participants = request.POST.getlist('participants')
            for participant_id in participants:
                EventHandler.objects.create(event=evt, client_id=participant_id)

            django_messages.success(request, f"Захід '{evt.theme}' створено!")
        except Exception as e:
            django_messages.error(request, f"Помилка створення заходу: {e}")
    return redirect('dashboard')


def edit_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        try:
            event = Event.objects.get(eventid=event_id)
            if str(event.author.clientid) == str(request.session.get('user_id')) or request.session.get('db_role') in [
                'Lead', 'Manager']:
                event.theme = request.POST.get('theme')
                event.description = request.POST.get('description')
                event.priority = request.POST.get('priority')
                event.date = request.POST.get('date')
                event.duration = request.POST.get('duration')
                event.link = request.POST.get('link')
                event.save()
                django_messages.success(request, f"Захід '{event.theme}' оновлено!")
            else:
                django_messages.error(request, "У вас немає прав редагувати цей захід")
        except Exception as e:
            django_messages.error(request, f"Помилка редагування: {e}")
    return redirect('dashboard')


def delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        try:
            event = Event.objects.get(eventid=event_id)
            theme = event.theme
            event.delete()
            django_messages.success(request, f"Захід '{theme}' видалено")
        except Exception as e:
            django_messages.error(request, f"Помилка видалення заходу: {e}")
    return redirect('dashboard')


def get_event_participants(request, event_id):
    try:
        participants = EventHandler.objects.filter(event_id=event_id).select_related('client')
        data = {
            'participants': [
                {'id': p.client.clientid, 'name': p.client.name, 'surname': p.client.surname}
                for p in participants
            ]
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def add_event_participant(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        client_id = request.POST.get('client_id')
        try:
            if not EventHandler.objects.filter(event_id=event_id, client_id=client_id).exists():
                EventHandler.objects.create(event_id=event_id, client_id=client_id)
                django_messages.success(request, "Учасника додано!")
            else:
                django_messages.warning(request, "Цей учасник вже доданий")
        except Exception as e:
            django_messages.error(request, f"Помилка додавання: {e}")
    return redirect('dashboard')


def remove_event_participant(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        client_id = request.POST.get('client_id')
        try:
            EventHandler.objects.filter(event_id=event_id, client_id=client_id).delete()
            django_messages.success(request, "Учасника видалено з заходу")
        except Exception as e:
            django_messages.error(request, f"Помилка: {e}")
    return redirect('dashboard')
