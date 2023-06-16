from .integrations.todoist import TodoistService
from .integrations.microsoft_todo import MicrosoftTodoService


class TodoServiceFactory:
    services = {
        'TODOIST': TodoistService,
        'MICROSOFT_TODO': MicrosoftTodoService,
    }

    @classmethod
    def get_service(cls, integration_type, *args, **kwargs):
        service_class = cls.services.get(integration_type)
        if not service_class:
            raise ValueError(f'Unknown integration type: {integration_type}')
        return service_class(*args, **kwargs)