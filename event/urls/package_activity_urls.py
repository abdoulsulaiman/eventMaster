from django.contrib import admin
from django.urls import path
from event.views import packageActivityViews


urlpatterns = [
    path('package_activities/add', packageActivityViews.addPackageActity.as_view())
]