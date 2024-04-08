
from django.db import models
from Event_master.metadata import MetaData
from Event_master.profile import Profile
import datetime

 

class Client(MetaData,Profile):
     
    NationalId=models.CharField(max_length=100,null=False,blank=False)
    identityType=models.CharField(max_length=100,null=False,blank=False)
    birth_date=models.CharField(max_length=100)
    names=models.CharField(max_length=200,null=False,blank=False)
    email=models.CharField(max_length=100,null=False,blank=False)
    address=models.DateTimeField(editable=True,null=True)
    tinNumber=models.CharField(max_length=100,null=True,blank=False)
    category = models.CharField(max_length=50, choices=[('Client', 'Client'), ('Organizer', 'Organizer')])
   

    def __str__(self):
        return self.firstName

    class Meta:
        db_table = "client"


    @staticmethod
    def all_clients():
        return Client.objects.filter(deleted_status=False)
