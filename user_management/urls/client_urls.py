from django.contrib import admin
from django.urls import path
from user_management.views import clientViews


urlpatterns = [
    path('clients', clientViews.client_list.as_view()),
    path('registration', clientViews.registerInstitution.as_view()),
    path('clients/<str:uuid>/become_organizer',clientViews.beOrganizer.as_view())

]