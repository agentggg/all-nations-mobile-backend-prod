from rest_framework import serializers
from .models import *

class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact 
        fields = '__all__'

class CategoryGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = CategoryGroup
        fields = '__all__'
        

class OutreachRegistration_FormSerializers(serializers.ModelSerializer):
    class Meta:
        model = OutreachRegistrationForm
        fields = '__all__'