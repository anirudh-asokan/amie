from .base import TodoService


class MicrosoftTodoService(TodoService):
    label = 'MICROSOFT_TODO'
    human_readable_name = 'Microsoft To Do'

    def sync_todo(self, todo, created, integration):
        pass

    def delete_todo(self, todo):
        pass
