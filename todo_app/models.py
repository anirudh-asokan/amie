from django.db import models
from .services import TodoistService, MicrosoftTodoService

##### User-Related Models #####

class User(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=128)
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been authenticated.
        """
        return True

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False


##### Task-Related Models #####

class TaskList(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_lists')
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks')
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)





##### Third-Party Integration Models #####

class ThirdPartyIntegration(models.Model):
    # Choices for the type of integration
    TODOIST = TodoistService.label
    MICROSOFT_TODO = MicrosoftTodoService.label
    INTEGRATION_CHOICES = [
        (TodoistService.label, TodoistService.human_readable_name),
        (MicrosoftTodoService.label, MicrosoftTodoService.human_readable_name),
    ]
    
    # Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='integrations')
    integration_type = models.CharField(max_length=20, choices=INTEGRATION_CHOICES)
    auth_token = models.CharField(max_length=255)  # Store authentication tokens or keys
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)