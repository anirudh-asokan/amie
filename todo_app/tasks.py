import logging
from .models import User, Task, TaskList, ThirdPartyIntegration
from .services import TodoServiceFactory
from celery import shared_task

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_integration_service(integration):
    return TodoServiceFactory.get_service(
        integration.integration_type, integration.auth_token, integration.user
    )


def handle_integration_task(integration_id, action_name, action):
    try:
        integration = ThirdPartyIntegration.objects.get(pk=integration_id)
        integration_service = get_integration_service(integration)
        integration_name = integration.get_integration_type_display()
        logger.info(f'{action_name} with {integration_name}')
        action(integration_service)
    except Exception as e:
        logger.error(f'Error during {action_name}: {e}')


@shared_task(bind=True, max_retries=3)
def push_task(self, task_id, created, integration_id):
    task = Task.objects.get(pk=task_id)
    handle_integration_task(
        integration_id,
        'Syncing task',
        lambda integration_service: integration_service.push_task(
            task, created)
    )


@shared_task(bind=True, max_retries=3)
def push_task_list(self, task_list_id, created, integration_id):
    task_list = TaskList.objects.get(pk=task_list_id)
    handle_integration_task(
        integration_id,
        'Syncing task list',
        lambda integration_service: integration_service.push_task_list(
            task_list, created)
    )


@shared_task(bind=True, max_retries=3)
def pull_task(self, integration_id):
    handle_integration_task(
        integration_id,
        'Pulling task',
        lambda integration_service: integration_service.pull_task()
    )


def query_pull_task(user):
    """
    Query all integrations associated with the user and pull tasks from them.
    This function is idempotent - it can be called multiple times without
    different side effects.
    """
    user_integrations = ThirdPartyIntegration.objects.filter(user=user)
    for integration in user_integrations:
        pull_task.delay(integration.id)


@shared_task
def query_pull_task_for_all_users():
    """
    Sync tasks and task lists for all users from third-party integrations.

    This function iterates through all users and synchronizes their tasks and 
    task lists with the third-party integrations they have added.

    It is meant to be executed periodically and is configured to run every hour
    via Django settings.
    """
    for user in User.objects.all():
        query_pull_task(user)
