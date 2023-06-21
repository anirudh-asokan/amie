import logging
from .base import TodoService
from todoist_api_python.api import TodoistAPI
from ..models.integration_models import ThirdPartyEntityMapping
from ..models.task_models import Task, TaskList

logger = logging.getLogger(__name__)


class TodoistService(TodoService):

    def __init__(self, integration):
        self.integration = integration
        self.api = TodoistAPI(integration.auth_token.token)
        self.user = integration.user

    def push_task(self, task, created):
        if created:
            task_todoist_id = ThirdPartyEntityMapping.get_third_party_id(
                task, self.integration)
            if task_todoist_id:
                # If created at Todoist, do not push it back to Todoist
                return
            self._create_task(task)
        else:
            self._update_task(task)

    def _create_task(self, task):
        try:
            task_list_todoist_id = ThirdPartyEntityMapping.get_third_party_id(
                task.tasklist, self.integration)
            todoist_task = self.api.add_task(
                content=task.title, project_id=task_list_todoist_id)
            logger.info(f'Task created: {todoist_task}')

            # Create ThirdPartyEntityMapping
            ThirdPartyEntityMapping.create_mapping(
                task, str(todoist_task.id), self.integration)
        except Exception as error:
            logger.error(f'Error creating task: {error}')
            task.delete()

    def _update_task(self, task):
        task_todoist_id = ThirdPartyEntityMapping.get_third_party_id(
            task, self.integration)
        try:
            is_update_success = self.api.update_task(
                task_id=task_todoist_id, content=task.title)
            is_close_success = True if not task.completed else self.api.close_task(
                task_id=task_todoist_id)

            if not is_update_success or not is_close_success:
                logger.warning('Task update or closure failed.')
        except Exception as error:
            logger.error(f'Error updating task: {error}')

    def pull_task(self):
        self._sync_projects()
        self._sync_tasks()

    def _sync_projects(self):
        try:
            todoist_projects = self.api.get_projects()
            todoist_project_ids = {int(project.id)
                                   for project in todoist_projects}

            for project in todoist_projects:
                self._create_or_update_project(project)

            self._delete_non_existent_projects(todoist_project_ids)
        except Exception as error:
            logger.error(f'Error syncing projects: {error}')

    def _create_or_update_project(self, todoist_project):
        # TODO: check timestamp to make sure old changes are not saved.
        task_list = ThirdPartyEntityMapping.get_trackable_entity(
            str(todoist_project.id), self.integration)
        if not task_list:
            task_list = TaskList.objects.create(
                title=todoist_project.name, user=self.user)
            ThirdPartyEntityMapping.create_mapping(
                task_list, str(todoist_project.id), self.integration)
        else:
            task_list.title = todoist_project.name
            task_list.save()

    def _delete_non_existent_projects(self, todoist_project_ids):
        for task_list in TaskList.objects.filter(user=self.user):
            task_list_todoist_id = ThirdPartyEntityMapping.get_third_party_id(
                task_list, self.integration)
            if int(task_list_todoist_id) not in todoist_project_ids:
                logger.error(f'{task_list_todoist_id} {todoist_project_ids}')
                task_list.delete()

    def _sync_tasks(self):
        try:
            todoist_tasks = self.api.get_tasks()
            todoist_task_ids = {int(task.id) for task in todoist_tasks}

            for todoist_task in todoist_tasks:
                self._create_or_update_task(todoist_task)

            self._mark_completed_non_existent_tasks(todoist_task_ids)
        except Exception as error:
            logger.error(f'Error syncing tasks: {error}')

    def _create_or_update_task(self, todoist_task):
        task_list = ThirdPartyEntityMapping.get_trackable_entity(
            str(todoist_task.project_id), self.integration)
        logger.error(f'Got parent task list: {task_list}')
        task = ThirdPartyEntityMapping.get_trackable_entity(
            str(todoist_task.id), self.integration)
        logger.error(f'Task is here or not -: {task}')

        # TODO - Also to check task_list exists
        if not task:

            task = Task.objects.create(
                title=todoist_task.content, user=self.user, tasklist=task_list, completed=todoist_task.is_completed)
            ThirdPartyEntityMapping.create_mapping(
                task, str(todoist_task.id), self.integration)
        else:
            task.title = todoist_task.content
            task.completed = todoist_task.is_completed
            task.tasklist = task_list
            task.save()

    def _mark_completed_non_existent_tasks(self, todoist_task_ids):
        for task in Task.objects.filter(user=self.user):
            task_todoist_id = ThirdPartyEntityMapping.get_third_party_id(
                task, self.integration)
            if int(task_todoist_id) not in todoist_task_ids:
                task.completed = True
                task.save()

    def push_task_list(self, task_list, created):
        if created:
            task_list_todoist_id = ThirdPartyEntityMapping.get_third_party_id(
                task_list, self.integration)
            if task_list_todoist_id:
                # If created at Todoist, do not push it back to Todoist
                return
            self._create_task_list(task_list)
        else:
            self._update_task_list(task_list)

    def _create_task_list(self, task_list):
        try:
            todoist_project = self.api.add_project(task_list.title)
            logger.info(f'Project created: {todoist_project}')

            # Create ThirdPartyEntityMapping
            ThirdPartyEntityMapping.create_mapping(
                task_list, str(todoist_project.id), self.integration)
        except Exception as error:
            logger.error(f'Error creating project: {error}')
            task_list.delete()

    def _update_task_list(self, task_list):
        task_list_todoist_id = ThirdPartyEntityMapping.get_third_party_id(
            task_list, self.integration)
        try:
            is_success = self.api.update_project(
                project_id=task_list_todoist_id, name=task_list.title)
            if not is_success:
                logger.warning('Project update failed.')
        except Exception as error:
            logger.error(f'Error updating project: {error}')
