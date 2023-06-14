from celery import shared_task
from .services import TodoServiceFactory

@shared_task
def sync_todo_task(task, created, integration):
    # Get the appropriate service for the integration type
    todo_service = TodoServiceFactory.get_service(integration.integration_type)

    # Sync the task
    todo_service.sync_todo(task, created, integration)