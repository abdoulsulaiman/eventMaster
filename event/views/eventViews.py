from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from django.contrib.auth.models import Permission
from rest_framework import status
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from event.models.event_type import EventType
from event.models.activity import Activity
from user_management.models.digital_profile import DigitalProfile
from user_management.models.client import Client
from event.models.event import Event
from event.serializers import PackageActivitySerializer,PackageSerializer,ActivitySerializer,CreatePackageActivitySerializer,CreateEventSerializer,EventSerializer,EventTypeSerializer
from  datetime import datetime

def getProfile(user):
        profile = get_object_or_404(
            DigitalProfile, user=user, deleted_status=False,referenceName='Organizer')
        return profile

class eventList(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]
    # permissions = ['admin.add_logentry']

    def get(self,*args, **kwargs):
        events = Event.objects.filter(deleted_status=False)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class addEvent(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]
    # permissions = ['admin.add_logentry']

    def post(self,*args, **kwargs):
        logprofile=getProfile(self.request.user)
        if not (Event.objects.filter(name=self.request.data['event_name'],referenceId=logprofile.referenceId)).exists():
            serializer = CreateEventSerializer(
                data=self.request.data)
            if serializer.is_valid():
                profile=DigitalProfile.objects.get(user=self.request.user,deleted_status=False,referenceName='Organizer')
                if profile is not None:
                    event = serializer.create(profile.referenceId)
                    return Response(data=EventSerializer(event).data, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse("Not Allowed to Create Event", safe=False, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse("Event With Entered Name Already Exists", safe=False, status=status.HTTP_400_BAD_REQUEST)

class eventCategoryList(APIView):
 
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]
    
    def get(self, *args, **kwargs):
            events = Event.objects.filter(deleted_status=False,eventCategory=self.kwargs['category'])
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)



class eventByTypesList(APIView):
 
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]
    
    def get(self, *args, **kwargs):
            events = Event.objects.filter(deleted_status=False,type__id=self.kwargs['type_id'])
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)



class event_details(APIView):
    
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]


    def get(self, *args, **kwargs):
        event = get_object_or_404(
            Event, uuid=self.kwargs['uuid'], deleted_status=False)
        acctype_serializer = EventSerializer(event)
        return JsonResponse(acctype_serializer.data, safe=False, status=status.HTTP_200_OK)



    def delete(self, *args, **kwargs):
        try:
            event = get_object_or_404(
                Event, uuid=self.kwargs['uuid'], deleted_status=False)
            event.deleted_status = True
            event.save()
            return JsonResponse(data="Event Deleted successfuly", safe=False,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse(data="Internal Server Error", safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
