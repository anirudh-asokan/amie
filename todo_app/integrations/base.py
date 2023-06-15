class TodoService:
    def push_task(self, task, created, integration):
        raise NotImplementedError

    def pull_task(self, integration):
        raise NotImplementedError

    def close_task(self, task, integration):
        raise NotImplementedError
    
    def push_task_list(self, task_list, created, integration):
        raise NotImplementedError