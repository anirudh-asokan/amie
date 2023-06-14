import graphene
from graphene_django import DjangoObjectType
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


# Queries
class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType, completed=graphene.Boolean(), task_list_id=graphene.Int())
    users = graphene.List(UserType)
    task_lists = graphene.List(TaskListType)


    def resolve_tasks(self, info, completed=None, task_list_id=None, **kwargs):
        # Filter based on whether the tasks are completed or not
        queryset = Task.objects.all()
        if completed is not None:
            queryset = queryset.filter(completed=completed)
        if task_list_id is not None:
            queryset = queryset.filter(tasklist_id=task_list_id)
        return queryset

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_task_lists(self, info, **kwargs):
        return TaskList.objects.all()

# Mutations
class CreateTaskWithReferences(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        title = graphene.String()
        user_id = graphene.Int()
        task_list_id = graphene.Int()

    def mutate(self, info, title, user_id, task_list_id):
        user = User.objects.get(pk=user_id)
        task_list = TaskList.objects.get(pk=task_list_id)
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
        task = Task.objects.get(pk=task_id)
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
        task = Task.objects.get(pk=task_id)
        task.completed = True
        task.save()
        return MarkTaskDone(task=task)

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String()
        full_name = graphene.String()
        password_hash = graphene.String()

    def mutate(self, info, email, full_name, password_hash):
        user = User(email=email, full_name=full_name, password_hash=password_hash)
        user.save()
        return CreateUser(user=user)


class CreateTaskList(graphene.Mutation):
    task_list = graphene.Field(TaskListType)

    class Arguments:
        title = graphene.String()
        user_id = graphene.Int()

    def mutate(self, info, title, user_id):
        user = User.objects.get(pk=user_id)
        task_list = TaskList(title=title, user=user)
        task_list.save()
        return CreateTaskList(task_list=task_list)


# Mutation Object
class Mutation(graphene.ObjectType):
    create_task_with_references = CreateTaskWithReferences.Field()
    update_task = UpdateTask.Field()
    mark_task_done = MarkTaskDone.Field()
    create_user = CreateUser.Field()
    create_task_list = CreateTaskList.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
