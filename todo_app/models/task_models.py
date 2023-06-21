from django.db import models
from .user_models import User


class TaskList(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_lists')
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    title = models.CharField(max_length=300)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks', null=True)
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
