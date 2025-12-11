from django.shortcuts import redirect
from django.contrib import messages as django_messages
from django.db import connection
from core.models import Client, Message


def add_user(request):
    if request.session.get('db_role') != 'Lead':
        django_messages.error(request, "Тільки тімлид може змінювати ролі")
        return redirect('dashboard')

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            email = request.POST.get('email')
            raw_password = request.POST.get('password')
            role_input = request.POST.get('role')

            client = Client.objects.create(
                name=name,
                surname=surname,
                email=email,
                role=role_input
            )

            db_user = f"user_{client.clientid}"
            safe_password = raw_password.replace("'", "''")

            with connection.cursor() as cursor:
                cursor.execute("RESET ROLE")
                cursor.execute(
                    f'CREATE ROLE "{db_user}" WITH LOGIN PASSWORD \'{safe_password}\' IN ROLE "{role_input}";')
                cursor.execute(f'GRANT "{db_user}" TO "connect_user";')

            django_messages.success(request, f"Користувача додано. Роль у базі даних: {db_user}")
        except Exception as e:
            django_messages.error(request, f"Помилка додавання користувача: {e}")
    return redirect('dashboard')


def delete_user(request):
    if request.session.get('db_role') != 'Lead':
        django_messages.error(request, "Тільки тімлид може змінювати ролі")
        return redirect('dashboard')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = Client.objects.get(clientid=user_id)
            db_user = f"user_{user.clientid}"

            with connection.cursor() as cursor:
                cursor.execute("RESET ROLE")
                cursor.execute(f'REASSIGN OWNED BY "{db_user}" TO "connect_user";')
                cursor.execute(f'DROP OWNED BY "{db_user}";')
                cursor.execute(f'DROP ROLE IF EXISTS "{db_user}";')

            user.delete()
            django_messages.success(request, f"Користувача видалено")
        except Exception as e:
            django_messages.error(request, f"Error deleting user: {e}")
    return redirect('dashboard')


def change_user_role(request):
    if request.session.get('db_role') != 'Lead':
        django_messages.error(request, "Тільки тімлид може змінювати ролі")
        return redirect('dashboard')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        try:
            user = Client.objects.get(clientid=user_id)
            old_role = user.role
            db_user = f"user_{user.clientid}"

            user.role = new_role
            user.save()

            with connection.cursor() as cursor:
                cursor.execute("RESET ROLE")
                cursor.execute(f'REVOKE "{old_role}" FROM "{db_user}"')
                cursor.execute(f'GRANT "{new_role}" TO "{db_user}"')

            django_messages.success(request, f"Роль змінено: {old_role} -> {new_role}")
        except Exception as e:
            django_messages.error(request, f"Error changing role: {e}")
    return redirect('dashboard')


def send_message(request):
    if request.method == 'POST':
        try:
            receiver_id = request.POST.get('receiver')
            title = request.POST.get('title')
            text = request.POST.get('text')
            sender_id = request.session.get('user_id')

            if not all([receiver_id, title, text, sender_id]):
                django_messages.error(request, "Заповніть усі поля")
                return redirect('dashboard')

            Message.objects.create(
                sender_id=sender_id,
                receiver_id=receiver_id,
                title=title,
                text=text
            )

            django_messages.success(request, "Повідомлення надіслано!")
        except Exception as e:
            django_messages.error(request, f"Error: {e}")
    return redirect('dashboard')
