from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, ThirdPartyIntegration
from .services import TodoServiceFactory
from .tasks import sync_todo_task

@receiver(post_save, sender=Task)
def sync_task(sender, instance, created, **kwargs):
    # Query all integrations associated with the user
    task = instance
    task_id = task.id

    user_integrations = ThirdPartyIntegration.objects.filter(user=task.user)

    # Iterate through each integration and sync the task
    for integration in user_integrations:
        sync_todo_task.delay(task_id, created, integration.id)
