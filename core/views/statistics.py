from django.shortcuts import render, redirect
from django.db.models import Q
from core.models import Client, Team, Project, Task, UnderTask


def view_statistics(request):
    role = request.session.get('db_role')
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    context = {
        'role': role,
        'user': Client.objects.get(clientid=user_id),
    }

    try:
        if role == 'Lead':
            context['team_stats'] = []
            teams = Team.objects.all()
            for team in teams:
                members = Client.objects.filter(teamhandler__team=team)
                projects = Project.objects.filter(projecthandler__team=team)
                tasks = Task.objects.filter(project__in=projects)

                context['team_stats'].append({
                    'team': team,
                    'members_count': members.count(),
                    'projects_count': projects.count(),
                    'tasks_total': tasks.count(),
                    'tasks_done': tasks.filter(status='Done').count(),
                    'tasks_active': tasks.filter(status__in=['To Do', 'In Progress', 'Review']).count(),
                })

            context['worker_stats'] = []
            workers = Client.objects.filter(role__in=['Developer', 'Manager'])
            for worker in workers:
                tasks_assigned = Task.objects.filter(taskhandler__client=worker)
                undertasks = UnderTask.objects.filter(developer=worker)

                context['worker_stats'].append({
                    'worker': worker,
                    'tasks_total': tasks_assigned.count(),
                    'tasks_done': tasks_assigned.filter(status='Done').count(),
                    'undertasks_total': undertasks.count(),
                    'undertasks_done': undertasks.filter(status='Done').count(),
                })

        elif role == 'Individual':
            my_tasks = Task.objects.filter(
                Q(undertask__author__clientid=user_id) | Q(taskhandler__client__clientid=user_id)
            ).distinct()

            context['my_stats'] = {
                'total_tasks': my_tasks.count(),
                'done_tasks': my_tasks.filter(status='Done').count(),
                'active_tasks': my_tasks.filter(status__in=['To Do', 'In Progress', 'Review']).count(),
                'canceled_tasks': my_tasks.filter(status='Canceled').count(),
            }

    except Exception as e:
        context['error'] = f"Помилка отримання статистики: {e}"

    return render(request, 'statistics.html', context)