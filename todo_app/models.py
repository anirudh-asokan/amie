from django.db import models
from .services import TodoistService, MicrosoftTodoService
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

##### User-Related Models #####

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

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