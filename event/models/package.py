
from django.db import models
from Event_master.metadata import MetaData
from Event_master.profile import Profile
import datetime

 
def wrapper(instance, filename):
    new_filename = str(datetime.datetime.now()).split(
        '.')[0]+'_'+str(instance.id).split('-')[0]+'__'+filename
    return 'EventImages/'+new_filename

CATEGORY_CHOICES = (
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
)


class Package(MetaData):
     
    name=models.CharField(max_length=100,null=False,blank=False)
   
   

    def __str__(self):
        return self.name

    class Meta:
        db_table = "package"
