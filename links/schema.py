import graphene
from graphene_django import DjangoObjectType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

# Define a mutation class
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    # Define data to send to the server
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    # Mutation method that creates a link in a DB 
    # thorugh url and description params
    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )

# Create Mutation class with a field to be resolved
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()