# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.db import connection
# from .models import Client
# from django.utils.text import slugify

# # Функція для безпечного створення SQL ідентифікаторів
# def quote_ident(text):
#     return f'"{text}"'

# @receiver(post_save, sender=Client)
# def manage_postgres_role(sender, instance, created, **kwargs):
#     # Визначаємо ім'я ролі (використовуємо email, бо він унікальний)
#     db_user = instance.Email
#     # Групова роль, яку наслідуємо (Developer, Manager...)
#     db_group = instance.Role 
#     # Пароль. УВАГА: Тут ми беремо хеш, але для справжнього логіну 
#     # в БД нам треба знати "чистий" пароль. 
#     # Оскільки Django зберігає тільки хеш, ми встановимо пароль для БД 
#     # такий самий, як хеш (або доведеться передавати raw_password через кастомний метод save).
#     # Для спрощення прикладу: припускаємо, що ми поки що ставимо dummy-пароль, 
#     # або ви передаєте raw_password у instance перед збереженням.
    
#     # Але оскільки нам треба логінитись, нам потрібен реальний пароль.
#     # Варіант: Вважаємо, що password у моделі Client зберігається в чистому вигляді 
#     # (що погано для безпеки, але необхідно для вашої архітектури, якщо ми не знаємо пароль при підключенні).
#     # АБО: Ви використовуєте механізм зміни пароля, який синхронізує його з БД.
    
#     # Припустимо, що у вас є доступ до чистого пароля під час створення (instance.password)
#     # Якщо ні - логін не спрацює.
    
#     password = instance.Password # Це поле має містити пароль, який прийме Postgres

#     with connection.cursor() as cursor:
#         if created:
#             # Створення користувача
#             # CREATE ROLE "user@email" WITH LOGIN PASSWORD 'pass' IN ROLE "Developer";
#             sql = f"""
#             CREATE ROLE {quote_ident(db_user)} 
#             WITH LOGIN PASSWORD '{password}' 
#             IN ROLE {quote_ident(db_group)};
#             """
#             cursor.execute(sql)
            
#             # Даємо доступ до схеми public, якщо його забрали у всіх
#             cursor.execute(f'GRANT USAGE ON SCHEMA public TO {quote_ident(db_user)};')
#         else:
#             # Оновлення (наприклад, змінилась група)
#             # Тут треба складнішу логіку ALTER ROLE, спрощено:
#             pass

# @receiver(post_delete, sender=Client)
# def delete_postgres_role(sender, instance, **kwargs):
#     db_user = instance.Email
#     with connection.cursor() as cursor:
#         # REASSIGN OWNED BY потрібен, щоб не втратити об'єкти, створені юзером
#         cursor.execute(f'REASSIGN OWNED BY {quote_ident(db_user)} TO postgres;')
#         cursor.execute(f'DROP OWNED BY {quote_ident(db_user)};')
#         cursor.execute(f'DROP ROLE IF EXISTS {quote_ident(db_user)};')