import logging
from .base import TodoService

logger = logging.getLogger(__name__)


class TodoistService(TodoService):
    label = 'TODOIST'
    human_readable_name = 'Todoist'

    def sync_todo(self, todo, created, integration):
        logger.info(f'\n\nInside sync_todo TODOIST\n\n')

        if created:
            # Code to push new todo to Todoist
            pass
        else:
            # Code to update existing todo in Todoist
            pass

    def delete_todo(self, todo):
        # Code to delete todo in Todoist
        pass
