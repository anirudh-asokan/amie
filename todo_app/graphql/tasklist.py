import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.core.exceptions import PermissionDenied
from ..models import Task, TaskList


class TaskListType(DjangoObjectType):
    class Meta:
        model = TaskList

    def resolve_tasks(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise PermissionDenied(
                "You must be authenticated to perform this action.")

        # Order the tasks within each task list by the updated_at field
        return Task.objects.filter(tasklist=self, user=user, completed=False).order_by('last_updated')


class CreateTaskList(graphene.Mutation):
    task_list = graphene.Field(TaskListType)

    class Arguments:
        title = graphene.String()

    def mutate(self, info, title):
        user = info.context.user
        if not user.is_authenticated:
            raise PermissionDenied(
                "You must be authenticated to perform this action.")

        task_list = TaskList(title=title, user=user)
        task_list.save()
        return CreateTaskList(task_list=task_list)


def resolve_task_lists(self, info, **kwargs):
    user = info.context.user
    if not user.is_authenticated:
        raise PermissionDenied(
            "You must be authenticated to perform this action.")

    return TaskList.objects.filter(user=user).prefetch_related('tasks').order_by('-last_updated')
