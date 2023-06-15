class TodoService:
    def sync_todo(self, todo, created, integration):
        raise NotImplementedError

    def delete_todo(self, todo):
        raise NotImplementedError