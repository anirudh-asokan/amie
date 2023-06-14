class TodoService:
    def sync_todo(self, todo, created):
        raise NotImplementedError

    def delete_todo(self, todo):
        raise NotImplementedError


class TodoistService(TodoService):
    label = 'TODOIST'
    human_readable_name = 'Todoist'

    def sync_todo(self, todo, created):
        if created:
            # Code to push new todo to Todoist
            pass
        else:
            # Code to update existing todo in Todoist
            pass

    def delete_todo(self, todo):
        # Code to delete todo in Todoist
        pass


class MicrosoftTodoService(TodoService):
    label = 'MICROSOFT_TODO'
    human_readable_name = 'Microsoft To Do'

    def sync_todo(self, todo, created):
        pass

    def delete_todo(self, todo):
        pass


class TodoServiceFactory:
    services = {
        'TODOIST': TodoistService,
        'MICROSOFT_TODO': MicrosoftTodoService,
    }

    @classmethod
    def get_service(cls, integration_type):
        service = cls.services.get(integration_type)
        if not service:
            raise ValueError(f'Unknown integration type: {integration_type}')
        return service()
