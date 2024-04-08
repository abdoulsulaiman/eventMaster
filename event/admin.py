from django.contrib import admin
from event.models.event import Event
from event.models.ticket import Ticket
from event.models.event_ticket_category import EventTicketCategory
from event.models.package import Package
from event.models.activity import Activity
from event.models.package_activity import PackageActivity

# Register your models here.
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(EventTicketCategory)
admin.site.register(Package)
admin.site.register(Activity)
admin.site.register(PackageActivity)
