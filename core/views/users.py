from django.shortcuts import redirect
from django.contrib import messages as django_messages
from core.models import Client, Message
import hashlib


def add_user(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            email = request.POST.get('email')
            raw_password = request.POST.get('password')
            role_input = request.POST.get('role')
            pass_hash = hashlib.sha256(raw_password.encode()).hexdigest()

            Client.objects.create(
                name=name,
                surname=surname,
                email=email,
                password=pass_hash,
                role=role_input
            )
            django_messages.success(request, f"Співробітника {name} {surname} додано до системи!")
        except Exception as e:
            django_messages.error(request, f"Помилка додавання користувача: {e}")
    return redirect('dashboard')


def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = Client.objects.get(clientid=user_id)
            name = f"{user.name} {user.surname}"
            user.delete()
            django_messages.success(request, f"Користувача {name} видалено")
        except Exception as e:
            django_messages.error(request, f"Помилка видалення: {e}")
    return redirect('dashboard')


def change_user_role(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        try:
            user = Client.objects.get(clientid=user_id)
            old_role = user.role
            user.role = new_role
            user.save()
            django_messages.success(request, f"Роль {user.name} змінено: {old_role} → {new_role}")
        except Exception as e:
            django_messages.error(request, f"Помилка зміни ролі: {e}")
    return redirect('dashboard')


def send_message(request):
    if request.method == 'POST':
        try:
            receiver_id = request.POST.get('receiver')
            title = request.POST.get('title')
            text = request.POST.get('text')
            sender_id = request.session.get('user_id')

            if not all([receiver_id, title, text, sender_id]):
                django_messages.error(request, "Заповніть всі поля")
                return redirect('dashboard')

            Message.objects.create(
                sender_id=sender_id,
                receiver_id=receiver_id,
                title=title,
                text=text
            )

            receiver = Client.objects.get(clientid=receiver_id)
            django_messages.success(request, f"Повідомлення надіслано користувачу {receiver.name}!")
        except Exception as e:
            django_messages.error(request, f"Помилка надсилання: {e}")
    return redirect('dashboard')