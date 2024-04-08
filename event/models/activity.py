
from django.db import models
from Event_master.metadata import MetaData
from Event_master.profile import Profile
import datetime
from event.models.event import Event
from event.models.event_ticket_category import EventTicketCategory
from user_management.models.client import Client

 
 

class Activity(MetaData):
     
    name=models.CharField(max_length=100,null=False,blank=False)
   
    def __str__(self):
        return self.name

    class Meta:
        db_table = "activity"
