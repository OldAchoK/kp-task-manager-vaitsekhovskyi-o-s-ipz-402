from django.db import models

class Priority(models.TextChoices):
    EXTREME = 'Extreme', 'Extreme'
    HIGH = 'High', 'High'
    AVERAGE = 'Average', 'Average'
    LOW = 'Low', 'Low'

class Status(models.TextChoices):
    TODO = 'To Do', 'To Do'
    IN_PROGRESS = 'In Progress', 'In Progress'
    REVIEW = 'Review', 'Review'
    DONE = 'Done', 'Done'
    CANCELED = 'Canceled', 'Canceled'

class Role(models.TextChoices):
    NO_COMMERCE = 'No Commerce', 'No Commerce'
    DEVELOPER = 'Developer', 'Developer'
    MANAGER = 'Manager', 'Manager'
    LEAD = 'Lead', 'Lead'
    INDIVIDUAL = 'Individual', 'Individual'

class Client(models.Model):
    clientid = models.BigAutoField(primary_key=True, db_column='clientid')
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(unique=True, max_length=64)
    password = models.CharField(max_length=255)
    avatar = models.CharField(max_length=2048, default='idle.png')
    role = models.CharField(max_length=30, choices=Role.choices)

    class Meta:
        managed = False
        db_table = 'client'

    def __str__(self):
        return f"{self.name} {self.surname}"

class Team(models.Model):
    teamid = models.BigAutoField(primary_key=True, db_column='teamid')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'team'

    def __str__(self):
        return self.title

class TeamHandler(models.Model):
    id = models.BigAutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, db_column='teamid')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='clientid')

    class Meta:
        managed = False
        db_table = 'teamhandler'
        unique_together = (('team', 'client'),)

class Project(models.Model):
    projectid = models.BigAutoField(primary_key=True, db_column='projectid')
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    medialink = models.CharField(max_length=2048, blank=True, null=True)
    creationdate = models.DateField(auto_now_add=True)
    deadline = models.DateField()

    class Meta:
        managed = False
        db_table = 'project'

    def __str__(self):
        return self.title

class ProjectHandler(models.Model):
    id = models.BigAutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, db_column='teamid')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='projectid')

    class Meta:
        managed = False
        db_table = 'projecthandler'
        unique_together = (('team', 'project'),)

class Task(models.Model):
    taskid = models.BigAutoField(primary_key=True, db_column='taskid')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, db_column='projectid')
    title = models.CharField(max_length=100)
    priority = models.CharField(max_length=7, choices=Priority.choices)
    description = models.CharField(max_length=1500)
    creationdate = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    resultlink = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task'

    def __str__(self):
        return self.title

class TaskHandler(models.Model):
    id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_column='taskid')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='clientid')

    class Meta:
        managed = False
        db_table = 'taskhandler'
        unique_together = (('task', 'client'),)

class UnderTask(models.Model):
    undertaskid = models.BigAutoField(primary_key=True, db_column='undertaskid')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_column='taskid')
    developer = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True, related_name='undertasks_dev', db_column='developerid')
    author = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True, related_name='undertasks_author', db_column='authorid')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    creationdate = models.DateField(auto_now_add=True)
    completiondate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    resultlink = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'undertask'

class Message(models.Model):
    messageid = models.BigAutoField(primary_key=True, db_column='messageid')
    sender = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sent_messages', db_column='senderid')
    receiver = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='received_messages', db_column='receiverid')
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1500)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'message'

class Event(models.Model):
    eventid = models.BigAutoField(primary_key=True, db_column='eventid')
    priority = models.CharField(max_length=7, choices=Priority.choices)
    author = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='authorid')
    theme = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    date = models.DateTimeField()
    duration = models.DurationField()
    link = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event'

class EventHandler(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column='eventid')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='clientid')

    class Meta:
        managed = False
        db_table = 'eventhandler'
        unique_together = (('event', 'client'),)

class MediaLink(models.Model):
    medialinkid = models.BigAutoField(primary_key=True, db_column='medialinkid')
    url = models.CharField(max_length=2048)
    description = models.CharField(max_length=255, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, db_column='taskid')
    undertask = models.ForeignKey(UnderTask, on_delete=models.CASCADE, blank=True, null=True, db_column='undertaskid')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, blank=True, null=True, db_column='messageid')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True, db_column='eventid')

    class Meta:
        managed = False
        db_table = 'medialink'