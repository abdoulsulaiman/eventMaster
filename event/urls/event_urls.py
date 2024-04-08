from django.contrib import admin
from django.urls import path
from event.views import eventViews


urlpatterns = [
    path('events/add', eventViews.addEvent.as_view()),
    path('events', eventViews.eventList.as_view()),
    path('events/<str:uuid>', eventViews.event_details.as_view()),
    path('events/<str:category>/display', eventViews.eventCategoryList.as_view()),
    path('events/<str:type_id>/all/display', eventViews.eventByTypesList.as_view()),
     


]