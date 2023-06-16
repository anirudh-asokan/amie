from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, TaskList, ThirdPartyIntegration
from .tasks import push_task, push_task_list

# This receiver is triggered whenever a Task object is saved
# It syncs the task with all the user's third-party integrations
@receiver(post_save, sender=Task)
def post_task_save(sender, instance, created, **kwargs):
    task = instance
    task_id = task.id

    # Query all integrations associated with the user
    user_integrations = ThirdPartyIntegration.objects.filter(user=task.user)

    # Iterate through each integration and sync the task
    for integration in user_integrations:
        push_task.delay(task_id, created, integration.id)

# This receiver is triggered whenever a TaskList object is saved
# It syncs the task list with all the user's third-party integrations
@receiver(post_save, sender=TaskList)
def post_task_list_save(sender, instance, created, **kwargs):
    task_list = instance
    task_list_id = task_list.id

    # Query all integrations associated with the user
    user_integrations = ThirdPartyIntegration.objects.filter(user=task_list.user)

    # Iterate through each integration and sync the task list
    for integration in user_integrations:
        push_task_list.delay(task_list_id, created, integration.id)
