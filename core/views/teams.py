from django.shortcuts import redirect
from django.db import transaction
from django.contrib import messages as django_messages
from django.http import JsonResponse
from core.models import Team, TeamHandler, Client, Project, ProjectHandler, Task
from core.forms import TeamForm, ProjectForm


def create_team(request):
    if request.session.get('db_role') not in ['Lead', 'Manager']:
        django_messages.error(request, "У вас немає прав на створення команд")
        return redirect('dashboard')

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    team = form.save()
                    user_id = request.session.get('user_id')
                    TeamHandler.objects.create(team=team, client_id=user_id)

                    members = request.POST.getlist('members')
                    for member_id in members:
                        if member_id != str(user_id):
                            TeamHandler.objects.create(team=team, client_id=member_id)

                    django_messages.success(request, f"Команду '{team.title}' створено!")
            except Exception as e:
                django_messages.error(request, f"Помилка створення команди: {e}")
        else:
            django_messages.error(request, "Невірні дані форми")
    return redirect('dashboard')


def delete_team(request):
    if request.method == 'POST':
        if request.session.get('db_role') != 'Lead':
            django_messages.error(request, "Тільки Lead може видаляти команди")
            return redirect('dashboard')

        team_id = request.POST.get('team_id')
        try:
            Team.objects.get(teamid=team_id).delete()
            django_messages.success(request, "Команду видалено!")
        except Exception as e:
            django_messages.error(request, f"Помилка видалення: {e}")
    return redirect('dashboard')


def get_team_members(request, team_id):
    if request.session.get('db_role') not in ['Lead', 'Manager']:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    try:
        handlers = TeamHandler.objects.filter(team_id=team_id).select_related('client')
        members = [{
            'id': h.client.clientid,
            'name': h.client.name,
            'surname': h.client.surname,
            'role': h.client.role
        } for h in handlers]
        return JsonResponse({'members': members})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def add_team_member(request):
    if request.method == 'POST':
        if request.session.get('db_role') not in ['Lead', 'Manager']:
            django_messages.error(request, "Немає прав")
            return redirect('dashboard')

        team_id = request.POST.get('team_id')
        user_id = request.POST.get('user_id')
        try:
            if not TeamHandler.objects.filter(team_id=team_id, client_id=user_id).exists():
                TeamHandler.objects.create(team_id=team_id, client_id=user_id)
                django_messages.success(request, "Учасника додано!")
            else:
                django_messages.warning(request, "Користувач вже в команді")
        except Exception as e:
            django_messages.error(request, f"Помилка: {e}")
    return redirect('dashboard')


def remove_team_member(request):
    if request.method == 'POST':
        if request.session.get('db_role') not in ['Lead', 'Manager']:
            django_messages.error(request, "Немає прав")
            return redirect('dashboard')

        team_id = request.POST.get('team_id')
        client_id = request.POST.get('client_id')
        try:
            TeamHandler.objects.filter(team_id=team_id, client_id=client_id).delete()
            django_messages.success(request, "Учасника видалено з команди")
        except Exception as e:
            django_messages.error(request, f"Помилка: {e}")
    return redirect('dashboard')


def create_project(request):
    if request.session.get('db_role') not in ['Lead', 'Manager']:
        django_messages.error(request, "Немає прав")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    project = form.save()
                    team_id = request.POST.get('team_id')
                    if team_id:
                        ProjectHandler.objects.create(project=project, team_id=team_id)
                    django_messages.success(request, f"Проект '{project.title}' створено!")
            except Exception as e:
                django_messages.error(request, f"Помилка створення проекту: {e}")
        else:
            django_messages.error(request, "Невірні дані форми")
    return redirect('dashboard')


def complete_project(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        try:
            project = Project.objects.get(projectid=project_id)
            project.status = 'Done'
            project.save()
            Task.objects.filter(project=project, status__in=['To Do', 'In Progress', 'Review']).update(
                status='Canceled')
            django_messages.success(request, f"Проект '{project.title}' завершено!")
        except Exception as e:
            django_messages.error(request, f"Помилка завершення проекту: {e}")
    return redirect('dashboard')


def delete_project(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        if request.session.get('db_role') not in ['Lead', 'Manager']:
            django_messages.error(request, "Немає прав на видалення проекту")
            return redirect('dashboard')
        try:
            project = Project.objects.get(projectid=project_id)
            title = project.title
            project.delete()
            django_messages.success(request, f"Проект '{title}' видалено!")
        except Exception as e:
            django_messages.error(request, f"Помилка видалення: {e}")
    return redirect('dashboard')


def get_project_details(request, project_id):
    if request.session.get('db_role') not in ['Lead', 'Manager']:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    try:
        project = Project.objects.get(projectid=project_id)
        handlers = ProjectHandler.objects.filter(project=project).select_related('team')
        teams = [{'id': h.team.teamid, 'title': h.team.title} for h in handlers]
        task_count = Task.objects.filter(project=project).count()

        return JsonResponse({
            'id': project.projectid,
            'title': project.title,
            'task_count': task_count,
            'teams': teams
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def add_project_team(request):
    if request.method == 'POST':
        if request.session.get('db_role') not in ['Lead', 'Manager']:
            django_messages.error(request, "Немає прав")
            return redirect('dashboard')

        project_id = request.POST.get('project_id')
        team_id = request.POST.get('team_id')
        try:
            if not ProjectHandler.objects.filter(project_id=project_id, team_id=team_id).exists():
                ProjectHandler.objects.create(project_id=project_id, team_id=team_id)
                django_messages.success(request, "Команду прикріплено до проекту!")
            else:
                django_messages.warning(request, "Ця команда вже працює над проектом")
        except Exception as e:
            django_messages.error(request, f"Помилка: {e}")
    return redirect('dashboard')


def remove_project_team(request):
    if request.method == 'POST':
        if request.session.get('db_role') not in ['Lead', 'Manager']:
            django_messages.error(request, "Немає прав")
            return redirect('dashboard')

        project_id = request.POST.get('project_id')
        team_id = request.POST.get('team_id')
        try:
            ProjectHandler.objects.filter(project_id=project_id, team_id=team_id).delete()
            django_messages.success(request, "Команду відкріплено від проекту")
        except Exception as e:
            django_messages.error(request, f"Помилка: {e}")
    return redirect('dashboard')
