import graphene
from graphene_django import DjangoObjectType
from .models import *
 

class ContactType(DjangoObjectType):
    class Meta:
        model = Contact
        fields = ("first_name_info","last_name_info", "contact_category", "phone_number_info", "user", "contact_notes_info")

class OutreachRegistrationForm(DjangoObjectType):
    class Meta:
        model = OutreachRegistrationForm
        fields = ("outreach_first_name","outreach_last_name", "outreach_phone_number", "outreach_spot", "outreach_category","minister_category", "outreach_date", "outreach_time")

 
 
class Query(graphene.ObjectType):
    allContact = graphene.List(ContactType)
 
    def resolve_allContact(self,info):
        return Contact.objects.all()
 
schema = graphene.Schema(query=Query)