import graphene
from graphene_django import DjangoObjectType
from ..models import User
from django.contrib.auth.hashers import make_password


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


def resolve_users(self, info, **kwargs):
    # We don't support returning users
    # Remove this block after development
    return User.objects.all()
