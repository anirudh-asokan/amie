from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, ThirdPartyIntegration
from .services import TodoServiceFactory

@receiver(post_save, sender=Task)
def sync_task(sender, instance, created, **kwargs):
    # Query all integrations associated with the user
    task = instance
    user_integrations = ThirdPartyIntegration.objects.filter(user=task.user)

    # Iterate through each integration and sync the task
    for integration in user_integrations:
        # Get the appropriate service for the integration type
        todo_service = TodoServiceFactory.get_service(integration.integration_type)

        # Sync the task
        todo_service.sync_todo(task, created, integration)
