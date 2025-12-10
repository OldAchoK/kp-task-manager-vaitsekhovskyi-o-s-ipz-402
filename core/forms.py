from django import forms
from .models import Task, Message, Client, UnderTask, Event, Team, Project


class TaskForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Проект",
        required=True
    )
    assignee = forms.ModelChoiceField(
        queryset=Client.objects.filter(role='Developer'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Виконавець",
        required=False
    )

    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'priority', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва завдання'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Опис завдання'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Назва',
            'description': 'Опис',
            'priority': 'Пріоритет',
            'deadline': 'Термін виконання',
        }


class UnderTaskForm(forms.ModelForm):
    developer = forms.ModelChoiceField(
        queryset=Client.objects.filter(role='Developer'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Виконавець",
        required=True
    )

    class Meta:
        model = UnderTask
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва підзавдання'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Опис підзавдання'}),
        }
        labels = {
            'title': 'Назва',
            'description': 'Опис',
        }


class EventForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label="Учасники",
        required=False
    )

    class Meta:
        model = Event
        fields = ['theme', 'description', 'priority', 'date', 'duration', 'link']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '01:30:00'}),
            'theme': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема заходу'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Опис заходу'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://meet.google.com/...'}),
        }
        labels = {
            'theme': 'Тема',
            'description': 'Опис',
            'priority': 'Пріоритет',
            'date': 'Дата і час',
            'duration': 'Тривалість',
            'link': 'Посилання',
        }


class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Кому",
        required=True
    )

    class Meta:
        model = Message
        fields = ['receiver', 'title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема повідомлення'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Текст повідомлення'}),
        }
        labels = {
            'title': 'Тема',
            'text': 'Повідомлення',
        }


class AddExecutorForm(forms.Form):
    task_id = forms.IntegerField(widget=forms.HiddenInput())
    executor = forms.ModelChoiceField(
        queryset=Client.objects.filter(role='Developer'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Виконавець"
    )


class SubmitResultForm(forms.Form):
    task_id = forms.IntegerField(widget=forms.HiddenInput())
    result_link = forms.URLField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
        label="Посилання на результат"
    )


class StatusUpdateForm(forms.Form):
    task_id = forms.IntegerField(widget=forms.HiddenInput())
    status = forms.ChoiceField(
        choices=[
            ('To Do', 'To Do'),
            ('In Progress', 'In Progress'),
            ('Review', 'Review'),
            ('Done', 'Done'),
            ('Canceled', 'Canceled')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва команди'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Опис команди'}),
        }
        labels = {
            'title': 'Назва',
            'description': 'Опис',
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'deadline', 'medialink']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва проекту'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'medialink': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }
        labels = {
            'title': 'Назва проекту',
            'deadline': 'Термін виконання',
            'medialink': 'Медіа-посилання',
        }


class UserCreateForm(forms.Form):
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я'}),
        label='Ім\'я'
    )
    surname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
        label='Прізвище'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label='Пароль'
    )
    role = forms.ChoiceField(
        choices=[
            ('Developer', 'Developer'),
            ('Manager', 'Manager'),
            ('Lead', 'Lead'),
            ('Individual', 'Individual'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Роль'
    )


class ChangeRoleForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    role = forms.ChoiceField(
        choices=[
            ('Developer', 'Developer'),
            ('Manager', 'Manager'),
            ('Lead', 'Lead'),
            ('Individual', 'Individual'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Нова роль'
    )
