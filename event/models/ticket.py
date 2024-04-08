
from django.db import models
from Event_master.metadata import MetaData
from Event_master.profile import Profile
import datetime
from event.models.event import Event
from event.models.event_ticket_category import EventTicketCategory
from user_management.models.client import Client

 
def wrapper(instance, filename):
    new_filename = str(datetime.datetime.now()).split(
        '.')[0]+'_'+str(instance.id).split('-')[0]+'__'+filename
    return 'EventImages/'+new_filename

CATEGORY_CHOICES = (
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
)


class Ticket(MetaData):
     
    tickNumber=models.CharField(max_length=100,null=False,blank=False)
    paymentStatus=models.CharField(max_length=200,null=False,blank=False,choices=CATEGORY_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    eventTicketCategory=models.ForeignKey(EventTicketCategory, on_delete=models.CASCADE)
    used=models.BooleanField(default=False)

   

    def __str__(self):
        return self.tickNumber

    class Meta:
        db_table = "ticket"
