from .base import TodoService


class MicrosoftTodoService(TodoService):
    def push_task(self, task, created, integration):
        pass

    def pull_task(self, integration):
        pass

    def close_task(self, task, integration):
        pass
    
    def push_task_list(self, task_list, created, integration):
        pass