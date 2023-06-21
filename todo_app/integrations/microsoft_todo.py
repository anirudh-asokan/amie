from .base import TodoService


class MicrosoftTodoService(TodoService):

    def __init__(self, integration):
        pass

    def push_task(self, task, created, integration):
        pass

    def pull_task(self, integration):
        pass

    def push_task_list(self, task_list, created, integration):
        pass
