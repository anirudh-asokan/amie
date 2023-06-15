import logging
from .base import TodoService
from todoist_api_python.api import TodoistAPI
from ..models import Task, TaskList

logger = logging.getLogger(__name__)


class TodoistService(TodoService):
    def push_task(self, task, created, integration):
        if created:
            if task.todoist_id:
                return
            api = TodoistAPI(integration.auth_token)
            try:
                todoist_task = api.add_task(content=task.title,
                                            project_id=task.tasklist.todoist_id)
                logger.info(todoist_task)

                task.todoist_id = todoist_task.id
                task.save()
            except Exception as error:
                task.delete()

    def pull_task(self, integration):
        api = TodoistAPI(integration.auth_token)
        try:
            todoist_projects = api.get_projects()
            for todoist_project in todoist_projects:
                if not TaskList.objects.filter(todoist_id=todoist_project.id).exists():
                    task_list = TaskList(
                        title=todoist_project.name, user=integration.user, todoist_id=todoist_project.id)
                    task_list.save()
        except Exception as error:
            pass

        try:
            todoist_tasks = api.get_tasks()
            all_tasks = Task.objects.filter(user=integration.user)
            all_tasks.update(completed=True)
            for todoist_task in todoist_tasks:
                if not Task.objects.filter(todoist_id=todoist_task.id).exists():
                    task_list = TaskList.objects.filter(
                        todoist_id=todoist_task.project_id).first()
                    task = Task(title=todoist_task.content, completed=todoist_task.is_completed,
                                user=integration.user, tasklist=task_list, todoist_id=todoist_task.id)
                    task.save()
                else:
                    task = Task.objects.filter(todoist_id=todoist_task.id).first()
                    task.title = todoist_task.content
                    task.completed = todoist_task.is_completed
                    task.save()
        except Exception as error:
            pass

    def close_task(self, task, integration):
        api = TodoistAPI(integration.auth_token)
        try:
            is_success = api.close_task(task_id=task.todoist_id)
            if not is_success:
                task.restore()
        except Exception as error:
            task.restore()

    def push_task_list(self, task_list, created, integration):
        if created:
            if task_list.todoist_id:
                return
            api = TodoistAPI(integration.auth_token)
            try:
                todoist_project = api.add_project(task_list.title)
                logger.info(todoist_project)

                # To prevent recursive post_save loop
                task_list.todoist_id = todoist_project.id
                task_list.save(update_fields=['todoist_id'])
            except Exception as error:
                task_list.delete()
