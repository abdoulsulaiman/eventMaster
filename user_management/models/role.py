from django.db import models
from Event_master.metadata import MetaData


class Role(MetaData):
    name=models.CharField(max_length=100,null=False,blank=False)
    description=models.CharField(max_length=255,null=False,blank=False)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "role"
