from django.shortcuts import render, redirect
from django.db import connection
from django.conf import settings
from core.models import Client
import psycopg


def custom_login(request):
    error = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Client.objects.get(email=email)
            db_user = f"user_{user.clientid}"
            db_conf = settings.DATABASES['default']

            try:
                with psycopg.connect(
                        dbname=db_conf['NAME'],
                        user=db_user,
                        password=password,
                        host=db_conf['HOST'],
                        port=db_conf['PORT']
                ) as conn:
                    pass

                request.session['user_id'] = user.clientid
                request.session['db_role'] = user.role
                request.session['db_user'] = db_user

                return redirect('dashboard')

            except psycopg.OperationalError:
                error = 'Incorrect password'

        except Client.DoesNotExist:
            error = 'User not found'
        except Exception as e:
            error = f'System error: {e}'

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    with connection.cursor() as cursor:
        cursor.execute("RESET ROLE")
    request.session.flush()
    return redirect('login')
