import graphene
import graphql_jwt
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from graphene_django.views import HttpError
from django.core.exceptions import PermissionDenied
from ..models import Task, TaskList


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class CreateTaskWithReferences(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        title = graphene.String()
        task_list_id = graphene.Int()

    def mutate(self, info, title, task_list_id):
        user = info.context.user
        if not user.is_authenticated:
            raise HttpError.Unauthorized(
                "You must be authenticated to perform this action.")

        try:
            task_list = TaskList.objects.get(pk=task_list_id)
        except TaskList.DoesNotExist:
            raise GraphQLError("Task with the given ID does not exist.")

        task = Task(title=title, user=user, tasklist=task_list)
        task.save()
        return CreateTaskWithReferences(task=task)


class UpdateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        task_id = graphene.Int()
        title = graphene.String()
        completed = graphene.Boolean()

    def mutate(self, info, task_id, title=None, completed=None):
        user = info.context.user
        if not user.is_authenticated:
            raise HttpError.Unauthorized(
                "You must be authenticated to perform this action.")

        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise GraphQLError("Task with the given ID does not exist.")

        if task.user != user:
            raise PermissionDenied(
                "You do not have permission to modify this task.")

        if title is not None:
            task.title = title
        if completed is not None:
            task.completed = completed
        task.save()
        return UpdateTask(task=task)


class MarkTaskDone(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        task_id = graphene.Int()

    def mutate(self, info, task_id):
        user = info.context.user
        if not user.is_authenticated:
            raise HttpError.Unauthorized(
                "You must be authenticated to perform this action.")

        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise GraphQLError("Task with the given ID does not exist.")

        if task.user != user:
            raise PermissionDenied(
                "You do not have permission to modify this task.")

        task.completed = True
        task.save()

        return MarkTaskDone(task=task)


def resolve_tasks(self, info, completed=None, task_list_id=None, **kwargs):
    # Filter based on whether the tasks are completed or not

    user = info.context.user
    if not user.is_authenticated:
        raise HttpError.Unauthorized(
            "You must be authenticated to perform this action.")

    queryset = Task.objects.filter(user=user)

    if completed is not None:
        queryset = queryset.filter(completed=completed)
    if task_list_id is not None:
        queryset = queryset.filter(tasklist_id=task_list_id)

    return queryset
