from django.contrib import admin
from django.urls import path
from event.views import eventTypeViews


urlpatterns = [

 path('event_types', eventTypeViews.eventTypeList.as_view()),
    path('events_types/<str:pk>', eventTypeViews.event_type_details.as_view())

]