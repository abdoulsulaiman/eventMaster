

from django.db import models
from Event_master.metadata import MetaData
from Event_master.profile import Profile
import datetime
from event.models.event import Event
 
class EventTicketCategory(MetaData):
     
    name=models.CharField(max_length=100,null=False,blank=False)
    Quantity=models.IntegerField(default=0)
    Price=models.CharField(null=False,blank=False,max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "event_ticket_category"
