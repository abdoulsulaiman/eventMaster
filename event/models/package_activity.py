

from django.db import models
from Event_master.metadata import MetaData
from Event_master.profile import Profile
import datetime
from event.models.package import Package
from event.models.activity import Activity
 
class PackageActivity(MetaData):
     
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return self.package+""+self.activity.name

    class Meta:
        db_table = "package_activity"
