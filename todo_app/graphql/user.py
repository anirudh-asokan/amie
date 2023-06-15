import graphene
from django.contrib.auth.hashers import make_password
from graphene_django import DjangoObjectType
from django.core.exceptions import PermissionDenied
from ..models import User
from ..tasks import query_pull_task


class UserType(DjangoObjectType):
    class Meta:
        model = User


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


class TodistWebhook(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        pass

    def mutate(self, info):
        user = info.context.user
        if not user.is_authenticated:
            raise PermissionDenied(
                "You must be authenticated to perform this action.")

        query_pull_task(user)
        return CreateUser(user=user)
