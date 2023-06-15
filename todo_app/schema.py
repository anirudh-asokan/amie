import graphene
import graphql_jwt
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from graphene_django.views import HttpError
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from .models import Task, TaskList, User

# Types


class UserType(DjangoObjectType):
    class Meta:
        model = User


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class TaskListType(DjangoObjectType):
    class Meta:
        model = TaskList

    def resolve_tasks(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise HttpError.Unauthorized(
                "You must be authenticated to perform this action.")

        # Order the tasks within each task list by the updated_at field
        return Task.objects.filter(tasklist=self, user=user).order_by('last_updated')

# Queries


class Query(graphene.ObjectType):
    tasks = graphene.List(
        TaskType, completed=graphene.Boolean(), task_list_id=graphene.Int())
    users = graphene.List(UserType)
    task_lists = graphene.List(TaskListType)

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

    def resolve_users(self, info, **kwargs):
        # We don't support returning users
        # Remove this block after development
        return User.objects.all()

    def resolve_task_lists(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise HttpError.Unauthorized(
                "You must be authenticated to perform this action.")

        return TaskList.objects.filter(user=user).prefetch_related('tasks').order_by('-last_updated')

# Mutations


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


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String()
        full_name = graphene.String()
        password = graphene.String()

    def mutate(self, info, email, full_name, password):
        hashed_password = make_password(password)
        user = User(email=email, full_name=full_name, password=hashed_password)
        user.save()
        return CreateUser(user=user)


class CreateTaskList(graphene.Mutation):
    task_list = graphene.Field(TaskListType)

    class Arguments:
        title = graphene.String()

    def mutate(self, info, title):
        user = info.context.user
        if not user.is_authenticated:
            raise HttpError.Unauthorized(
                "You must be authenticated to perform this action.")

        task_list = TaskList(title=title, user=user)
        task_list.save()
        return CreateTaskList(task_list=task_list)


# Mutation Object
class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_task_with_references = CreateTaskWithReferences.Field()
    update_task = UpdateTask.Field()
    mark_task_done = MarkTaskDone.Field()
    create_user = CreateUser.Field()
    create_task_list = CreateTaskList.Field()


# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
