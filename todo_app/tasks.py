import logging
from celery import shared_task
from .models import Task, ThirdPartyIntegration
from .services import TodoServiceFactory

# Get an instance of a logger
logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def sync_todo_task(self, task_id, created, integration_id):
    # Retrieve the task and integration instances from their IDs
    task = Task.objects.get(pk=task_id)
    integration = ThirdPartyIntegration.objects.get(pk=integration_id)

    # Get the appropriate service for the integration type
    todo_service = TodoServiceFactory.get_service(integration.integration_type)

    try:
        # Sync the task
        integration_name = integration.get_integration_type_display()
        logger.info('Syncing with', integration_name)
        todo_service.sync_todo(task, created, integration)
    except Exception as e:
        raise self.retry(exc=e)
