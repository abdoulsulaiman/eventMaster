from django.db import models
from Event_master.metadata import MetaData
import datetime

from user_management.models.permission import Permission
from user_management.models.role import Role

class RolePermission(MetaData):
     
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
   

    def __str__(self):
        return self.role.name+""+self.permission.name

    class Meta:
        db_table = "role_permission"
