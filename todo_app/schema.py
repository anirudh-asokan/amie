import graphene
import graphql_jwt
from .graphql.user import UserType, CreateUser, TodistWebhook
from .graphql.task import TaskType, CreateTaskWithReferences, UpdateTask, MarkTaskDone, resolve_tasks
from .graphql.tasklist import TaskListType, CreateTaskList, resolve_task_lists


class Query(graphene.ObjectType):
    tasks = graphene.List(
        TaskType, completed=graphene.Boolean(), task_list_id=graphene.Int())
    users = graphene.List(UserType)
    task_lists = graphene.List(TaskListType)

    resolve_tasks = resolve_tasks
    resolve_task_lists = resolve_task_lists


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_task_with_references = CreateTaskWithReferences.Field()
    update_task = UpdateTask.Field()
    mark_task_done = MarkTaskDone.Field()
    create_user = CreateUser.Field()
    create_task_list = CreateTaskList.Field()
    todoist_webhook = TodistWebhook.Field()


# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
