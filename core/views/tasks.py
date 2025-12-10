from django.shortcuts import redirect
from django.db import transaction
from django.contrib import messages as django_messages
from core.models import Task, TaskHandler, UnderTask, Client
from core.forms import TaskForm, UnderTaskForm
import datetime


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    task = form.save(commit=False)
                    task.status = 'To Do'
                    task.save()

                    # Логика для добавления исполнителя или автора
                    user_role = request.session.get('db_role')
                    user_id = request.session.get('user_id')

                    assignee = form.cleaned_data.get('assignee')

                    # Если создал Individual, он автоматически прикрепляется, чтобы видеть задачу
                    if user_role == 'Individual':
                        TaskHandler.objects.create(task=task, client_id=user_id)

                    if assignee:
                        # Проверяем, чтобы не дублировать, если сам себе назначил
                        if not (user_role == 'Individual' and str(assignee.clientid) == str(user_id)):
                            TaskHandler.objects.create(task=task, client=assignee)

                django_messages.success(request, f"Завдання '{task.title}' створено!")
            except Exception as e:
                django_messages.error(request, f"Помилка створення завдання: {e}")
        else:
            django_messages.error(request, "Невірні дані форми")
    return redirect('dashboard')


def edit_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        try:
            task = Task.objects.get(taskid=task_id)
            task.title = request.POST.get('title')
            task.description = request.POST.get('description')
            task.priority = request.POST.get('priority')
            task.deadline = request.POST.get('deadline')
            task.save()
            django_messages.success(request, f"Завдання '{task.title}' оновлено!")
        except Exception as e:
            django_messages.error(request, f"Помилка редагування: {e}")
    return redirect('dashboard')


def update_task_status(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        new_status = request.POST.get('status')
        try:
            task = Task.objects.get(taskid=task_id)
            old_status = task.status
            task.status = new_status
            task.save()
            django_messages.success(request, f"Статус змінено: {old_status} → {new_status}")
        except Exception as e:
            django_messages.error(request, f"Помилка оновлення статусу: {e}")
    return redirect('dashboard')


def reject_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        reason = request.POST.get('reject_reason', 'Не вказано')
        try:
            task = Task.objects.get(taskid=task_id)
            task.status = 'To Do'
            task.description = f"{task.description}\n\n[ВІДХИЛЕНО]: {reason}"
            task.save()
            django_messages.warning(request, f"Завдання '{task.title}' відхилено. Причина: {reason}")
        except Exception as e:
            django_messages.error(request, f"Помилка: {e}")
    return redirect('dashboard')


def delete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        try:
            task = Task.objects.get(taskid=task_id)
            title = task.title
            task.delete()
            django_messages.success(request, f"Завдання '{title}' видалено")
        except Exception as e:
            django_messages.error(request, f"Помилка видалення: {e}")
    return redirect('dashboard')


def cancel_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        reason = request.POST.get('reason', 'Не вказано')
        try:
            task = Task.objects.get(taskid=task_id)
            task.status = 'Canceled'
            task.description = f"{task.description}\n\n[СКАСОВАНО]: {reason}"
            task.save()
            django_messages.warning(request, f"Завдання '{task.title}' скасовано. Причина: {reason}")
        except Exception as e:
            django_messages.error(request, f"Помилка скасування: {e}")
    return redirect('dashboard')


def submit_result(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        result_link = request.POST.get('result_link')
        try:
            task = Task.objects.get(taskid=task_id)
            task.resultlink = result_link
            task.status = 'Review'
            task.save()
            django_messages.success(request, f"Результат завдання '{task.title}' відправлено на перевірку!")
        except Exception as e:
            django_messages.error(request, f"Помилка здачі роботи: {e}")
    return redirect('dashboard')


def add_executor(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        executor_id = request.POST.get('executor')
        try:
            if not TaskHandler.objects.filter(task_id=task_id, client_id=executor_id).exists():
                TaskHandler.objects.create(task_id=task_id, client_id=executor_id)
                django_messages.success(request, "Виконавця додано до завдання!")
            else:
                django_messages.warning(request, "Цей виконавець вже призначений на завдання")
        except Exception as e:
            django_messages.error(request, f"Помилка додавання виконавця: {e}")
    return redirect('dashboard')


def remove_executor(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        executor_id = request.POST.get('executor_id')
        try:
            TaskHandler.objects.filter(task_id=task_id, client_id=executor_id).delete()
            django_messages.success(request, "Виконавця видалено з завдання")
        except Exception as e:
            django_messages.error(request, f"Помилка видалення виконавця: {e}")
    return redirect('dashboard')


def create_undertask(request):
    if request.method == 'POST':
        form = UnderTaskForm(request.POST)
        parent_task_id = request.POST.get('parent_task_id')
        if form.is_valid() and parent_task_id:
            try:
                ut = form.save(commit=False)
                ut.task_id = parent_task_id
                ut.author_id = request.session.get('user_id')
                ut.developer = form.cleaned_data['developer']
                ut.status = 'To Do'
                ut.save()
                django_messages.success(request, f"Підзавдання '{ut.title}' створено!")
            except Exception as e:
                django_messages.error(request, f"Помилка створення підзавдання: {e}")
        else:
            django_messages.error(request, "Невірні дані")
    return redirect('dashboard')


def submit_undertask_result(request):
    if request.method == 'POST':
        undertask_id = request.POST.get('undertask_id')
        result_link = request.POST.get('result_link')
        try:
            ut = UnderTask.objects.get(undertaskid=undertask_id)
            ut.resultlink = result_link
            ut.status = 'Review'
            ut.completiondate = datetime.date.today()
            ut.save()
            django_messages.success(request, f"Результат підзавдання '{ut.title}' відправлено на перевірку тімліду!")
        except Exception as e:
            django_messages.error(request, f"Помилка: {e}")
    return redirect('dashboard')


def update_undertask_status(request):
    if request.method == 'POST':
        undertask_id = request.POST.get('undertask_id')
        new_status = request.POST.get('status')
        try:
            ut = UnderTask.objects.get(undertaskid=undertask_id)
            ut.status = new_status
            if new_status == 'Done':
                ut.completiondate = datetime.date.today()
            ut.save()
            django_messages.success(request, f"Статус підзавдання оновлено!")
        except Exception as e:
            django_messages.error(request, f"Помилка: {e}")
    return redirect('dashboard')


def reject_undertask(request):
    if request.method == 'POST':
        undertask_id = request.POST.get('undertask_id')
        reason = request.POST.get('reject_reason', 'Не вказано')
        try:
            ut = UnderTask.objects.get(undertaskid=undertask_id)
            ut.status = 'To Do'
            ut.description = f"{ut.description}\n\n[ВІДХИЛЕНО]: {reason}"
            ut.save()
            django_messages.warning(request, f"Підзавдання '{ut.title}' відхилено. Причина: {reason}")
        except Exception as e:
            django_messages.error(request, f"Помилка: {e}")
    return redirect('dashboard')
