from .integrations.todoist import TodoistService
from .integrations.microsoft_todo import MicrosoftTodoService


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
