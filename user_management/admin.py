from django.contrib import admin
from user_management.models.client import Client
from user_management.models.permission import Permission
from user_management.models.role import Role
from user_management.models.role_permission import RolePermission
from user_management.models.digital_profile import DigitalProfile
from user_management.models.representative import Representative

# Register your models here.
admin.site.register(Client)
admin.site.register(Representative)
admin.site.register(DigitalProfile)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(RolePermission)