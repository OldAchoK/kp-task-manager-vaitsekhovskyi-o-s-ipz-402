from django.shortcuts import render, redirect
from django.db import connection
from core.models import Client
import hashlib


def custom_login(request):
    error = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            user = Client.objects.get(email=email)
            if user.password == pass_hash:
                request.session['user_id'] = user.clientid
                request.session['db_role'] = user.role
                return redirect('dashboard')
            else:
                error = 'Невірний пароль'
        except Client.DoesNotExist:
            error = 'Користувача не знайдено'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    with connection.cursor() as cursor:
        cursor.execute("RESET ROLE")
    request.session.flush()
    return redirect('login')