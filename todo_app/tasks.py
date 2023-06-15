import logging
from .models import User, Task, TaskList, ThirdPartyIntegration
from .services import TodoServiceFactory
from celery import shared_task

# Get an instance of a logger
logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def push_task(self, task_id, created, integration_id):
    # Retrieve the task and integration instances from their IDs
    task = Task.objects.get(pk=task_id)
    integration = ThirdPartyIntegration.objects.get(pk=integration_id)

    # Get the appropriate service for the integration type
    integration_service = TodoServiceFactory.get_service(integration.integration_type)

    try:
        # Push the task
        integration_name = integration.get_integration_type_display()
        logger.info(f'Syncing with {integration_name}')
        integration_service.push_task(task, created, integration)
    except Exception as e:
        raise self.retry(exc=e)


@shared_task(bind=True, max_retries=3)
def push_task_list(self, task_list_id, created, integration_id):
    # Retrieve the task list and integration instances from their IDs
    task_list = TaskList.objects.get(pk=task_list_id)
    integration = ThirdPartyIntegration.objects.get(pk=integration_id)

    # Get the appropriate service for the integration type
    integration_service = TodoServiceFactory.get_service(integration.integration_type)

    try:
        # Push the task list
        integration_name = integration.get_integration_type_display()
        logger.info(f'Syncing with {integration_name}')
        integration_service.push_task_list(task_list, created, integration)
    except Exception as e:
        raise self.retry(exc=e)


@shared_task(bind=True, max_retries=3)
def close_task(self, task_id, integration_id):
    # Retrieve the task and integration instances from their IDs
    task = Task.objects.get(pk=task_id)
    integration = ThirdPartyIntegration.objects.get(pk=integration_id)

    # Get the appropriate service for the integration type
    integration_service = TodoServiceFactory.get_service(integration.integration_type)

    try:
        # Close task
        integration_name = integration.get_integration_type_display()
        logger.info(f'Closing task on {integration_name}')
        integration_service.close_task(task, integration)
    except Exception as e:
        raise self.retry(exc=e)


def post_task_close(user, task):

    # Query all integrations associated with the user
    user_integrations = ThirdPartyIntegration.objects.filter(user=user)

    # Iterate through each integration and sync the task list
    for integration in user_integrations:
        close_task.delay(task.id, integration.id)


@shared_task(bind=True, max_retries=3)
def pull_task(self, integration_id):
    # Retrieve the integration instances from their ID
    integration = ThirdPartyIntegration.objects.get(pk=integration_id)

    # Get the appropriate service for the integration type
    integration_service = TodoServiceFactory.get_service(integration.integration_type)

    try:
        # Pull task
        integration_name = integration.get_integration_type_display()
        logger.info(f'Pull task from {integration_name}')
        integration_service.pull_task(integration)
    except Exception as e:
        raise self.retry(exc=e)
    

def query_pull_task(user):
    # Query all integrations associated with the user
    user_integrations = ThirdPartyIntegration.objects.filter(user=user)

    # Iterate through each integration and sync the task list
    for integration in user_integrations:
        pull_task.delay(integration.id)


# Run every hour
@shared_task
def query_pull_task_for_all_users():
    for user in User.objects.all():
        query_pull_task(user)
