from rest_framework import serializers
from user_management.models.client import Client
from datetime import datetime ,timedelta
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from user_management.models.digital_profile import DigitalProfile,User
from user_management.models.role import Role
from django.db import models
import uuid

def generate_default_password():
    return get_random_string(length=8)

class  ClientSerializer(serializers.ModelSerializer):
    last_updated_by = serializers.CharField(required=False, read_only=True)

    class Meta:
        model =Client
        fields='__all__'

 

class RegistrationSerializer(serializers.Serializer):
    names = serializers.CharField(max_length=150)
    firstName=serializers.CharField(max_length=100)
    lastName=serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=100)
    gender = serializers.CharField(max_length=100)
    user_name = serializers.CharField(max_length=100)
    password= serializers.CharField(max_length=100)
    dob=serializers.CharField(max_length=100)

    def create(self):
        
            client = Client()
            client.firstName=self.validated_data.pop("firstName")
            client.lastName=self.validated_data.pop("lastName")
            client.phone = self.validated_data.pop('phone_number')
            client.email = self.validated_data.pop('email')
            client.gender=self.validated_data.pop('gender')
            client.birth_date=self.validated_data.pop('dob')
            client.category="Client"
            client.save()
        

            new_user=User()
            new_user.first_name=self.validated_data.pop("firstName")
            new_user.last_name=self.validated_data.pop("lastName")
            new_user.email=self.validated_data.pop('email')
            new_user.phone_number=self.validated_data.pop('phone_number')
            new_user.username=self.validated_data.pop('user_name')
            new_user.set_password(self.validated_data.pop('password'))
            new_user.has_set_password=True
            new_user.referenceId=client.pk
            new_user.is_admin=True
            new_user.save()
            
            # Finding Role and Create if Doesn't Exist
            role=Role.objects.filter(pk=1).count()
            if role==0:
                new_role=Role()
                new_role.name="Basic"
                new_role.save()

            dprofile=DigitalProfile()
            dprofile.referenceId=client.pk
            dprofile.referenceName='Client'
            dprofile.role=Role.objects.get(pk=1)
            dprofile.user=new_user
            dprofile.save()
            return client

class ProfileData(models.Model):
    email = models.CharField(max_length=100,null=True)
    first_name = models.CharField(max_length=100,null=False,blank=False)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    phone_number=models.CharField(max_length=100,null=False,blank=False)
    username=models.CharField(max_length=100,null=False,blank=False)
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, blank=False, null=False)
    has_more_profile = models.BooleanField(default=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    is_superuser = models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileData
        fields = '__all__'

    
    def to_representation(self, instance):
        self.fields['client'] = ClientSerializer(read_only=True)
        return super(ProfileSerializer, self).to_representation(instance)
    

