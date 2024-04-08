
from django.db import models
from Event_master.metadata import MetaData
from Event_master.profile import Profile
import datetime
from user_management.models.client import Client
 

class Representative(MetaData,Profile):
     
    NationalId=models.CharField(max_length=100,null=False,blank=False)
    identityType=models.CharField(max_length=100,null=False,blank=False)
    birth_date=models.DateTimeField(editable=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    
   

    def __str__(self):
        return self.firstName

    class Meta:
        db_table = "representative"
