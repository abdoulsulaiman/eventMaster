from django.db import models
from Event_master.metadata import MetaData
import datetime
from rest_framework import serializers
from accounts.models import User
from user_management.models.role import Role
import uuid


class DigitalProfile(MetaData):
     
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    referenceId=models.CharField(max_length=100,null=False,blank=False)
    referenceName=models.CharField(max_length=100,null=False,blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   

    def __str__(self):
        return self.referenceName

    class Meta:
        db_table = "digital_profile"



