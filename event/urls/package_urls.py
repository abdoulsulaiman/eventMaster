from django.contrib import admin
from django.urls import path
from event.views import packageViews


urlpatterns = [
    path('packages', packageViews.package_list.as_view()),
    path('packages/<str:uuid>', packageViews.package_details.as_view()),
    path('packages/<str:pk>/activities', packageViews.GetPackageActivities.as_view()),
   
]