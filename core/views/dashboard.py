from django.shortcuts import render, redirect
from django.db.models import Q
from core.models import Client, Task, Project, Message, UnderTask, Event, Team
from core.forms import TaskForm, MessageForm, StatusUpdateForm, UnderTaskForm, EventForm, AddExecutorForm, \
    SubmitResultForm, ProjectForm, TeamForm
from datetime import datetime, timedelta


def dashboard(request):
    role = request.session.get('db_role', 'connect_user')
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = Client.objects.get(clientid=user_id)
    except Client.DoesNotExist:
        return redirect('logout')

    context = {
        'role': role,
        'user': user,
        'tasks': [],
        'projects': [],
        'messages_list': [],
        'events': [],
        'stats': None,
        'team_members': [],
        'teams': [],
        'undertasks': [],
        'forms': {
            'task': TaskForm(),
            'message': MessageForm(),
            'status': StatusUpdateForm(),
            'undertask': UnderTaskForm(),
            'event': EventForm(),
            'add_executor': AddExecutorForm(),
            'submit_result': SubmitResultForm(),
            'project': ProjectForm(),
            'team': TeamForm(),
        }
    }

    try:
        if role == 'Developer':
            tasks_query = Task.objects.filter(taskhandler__client__clientid=user_id).select_related('project')
            context['undertasks'] = UnderTask.objects.filter(developer__clientid=user_id).select_related('task',
                                                                                                         'author')

        elif role == 'Individual':
            tasks_query = Task.objects.all().select_related('project')
            context['undertasks'] = UnderTask.objects.all().select_related('task', 'author', 'developer')

        else:
            tasks_query = Task.objects.all().select_related('project')
            context['undertasks'] = UnderTask.objects.all().select_related('task', 'author', 'developer')

        project_filter = request.GET.get('project')
        if project_filter:
            tasks_query = tasks_query.filter(project_id=project_filter)

        priority_filter = request.GET.get('priority')
        if priority_filter:
            tasks_query = tasks_query.filter(priority=priority_filter)

        status_filter = request.GET.get('status')
        if status_filter:
            tasks_query = tasks_query.filter(status=status_filter)

        deadline_filter = request.GET.get('deadline')
        if deadline_filter:
            today = datetime.now().date()
            if deadline_filter == 'urgent':
                tasks_query = tasks_query.filter(deadline__lte=today + timedelta(days=3), deadline__gte=today)
            elif deadline_filter == 'soon':
                tasks_query = tasks_query.filter(deadline__lte=today + timedelta(days=7),
                                                 deadline__gt=today + timedelta(days=3))
            elif deadline_filter == 'later':
                tasks_query = tasks_query.filter(deadline__gt=today + timedelta(days=7))

        context['tasks'] = tasks_query.order_by('-creationdate')

        context['messages_list'] = Message.objects.filter(
            Q(receiver__clientid=user_id) | Q(sender__clientid=user_id)
        ).select_related('sender', 'receiver').order_by('-date')

        context['events'] = Event.objects.all().select_related('author').order_by('-date')

        context['projects'] = Project.objects.all()

        if role in ['Manager', 'Lead']:
            context['team_members'] = Client.objects.all()
            context['teams'] = Team.objects.all()

        if role == 'Lead':
            total_tasks = Task.objects.count()
            done_tasks = Task.objects.filter(status='Done').count()
            canceled_tasks = Task.objects.filter(status='Canceled').count()
            progress_percent = round((done_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0

            context['stats'] = {
                'total_tasks': total_tasks,
                'done': done_tasks,
                'canceled': canceled_tasks,
                'progress': progress_percent,
                'active_projects': Project.objects.filter(status='In Progress').count(),
                'total_projects': Project.objects.count(),
            }

        elif role == 'Individual':
            total_tasks = Task.objects.count()
            done_tasks = Task.objects.filter(status='Done').count()
            progress = round((done_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0

            context['stats'] = {
                'total_tasks': total_tasks,
                'done': done_tasks,
                'progress': progress,
                'active_projects': Project.objects.filter(status='In Progress').count()
            }

    except Exception as e:
        context['error'] = f"Помилка БД: {str(e)}"

    return render(request, 'dashboard.html', context)
