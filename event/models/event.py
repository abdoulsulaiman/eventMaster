
from django.db import models
from Event_master.metadata import MetaData
from Event_master.profile import Profile
from event.models.package import Package
from event.models.event_type import EventType
import datetime

 
def wrapper(instance, filename):
    new_filename = str(datetime.datetime.now()).split(
        '.')[0]+'_'+str(instance.id).split('-')[0]+'__'+filename
    return 'EventImages/'+new_filename




class Event(MetaData):
     
    name=models.CharField(max_length=100,null=False,blank=False)
    soldTickets=models.IntegerField(default=0)
    isPayableEvent=models.BooleanField(default=False)
    landingImage=models.ImageField(
        upload_to=wrapper, null=True, default=None)
    homeImage=models.ImageField(
        upload_to=wrapper, null=True, default=None)
    
    address=models.CharField(null=False,max_length=200)
    package=models.ForeignKey(Package, on_delete=models.CASCADE)
    referenceId=models.CharField(max_length=100,null=False,blank=False)
    eventCategory= models.CharField(max_length=200, choices=[('One-Day', 'One-Day'), ('Series', 'Series')], default='One-Day')
    type=models.ForeignKey(EventType, on_delete=models.CASCADE)
    will_be_there=models.IntegerField(default=0,null=False,blank=False)
   

    def __str__(self):
        return self.name

    class Meta:
        db_table = "event"
