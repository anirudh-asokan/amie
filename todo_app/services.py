from .integrations.todoist import TodoistService
from .integrations.microsoft_todo import MicrosoftTodoService


class TodoServiceFactory:
    services = {
        'TODOIST': TodoistService,
        'MICROSOFT_TODO': MicrosoftTodoService,
    }

    @classmethod
    def get_service(cls, third_party_app, *args, **kwargs):
        service_class = cls.services.get(third_party_app.service_key)
        if not service_class:
            raise ValueError(f'Unknown integration type: {third_party_app.service_key}')
        return service_class(*args, **kwargs)