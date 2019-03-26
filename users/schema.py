from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    """Defines user mutation"""
    user = graphene.Field(UserType)

    class Arguments:
        """Defines data to send to the server"""
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        """Creates a user in DB through username and email parameters"""
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    """Creates Mutation class with a filed to be resolved (create_user)"""
    create_user = CreateUser.Field()
