
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



class eventTypeList(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]
    
    def get(self, *args, **kwargs):
            eventTypes = EventType.all()
            serializer = EventTypeSerializer(eventTypes, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,*args, **kwargs):
        try:
            eventType=EventType()
            eventType.name=self.request.data['name']
            eventType.description=self.request.data['description']
            eventType.save()
            
            return JsonResponse(data=EventTypeSerializer(eventType).data, safe=False, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return JsonResponse(data=e, safe=False, status=status.HTTP_400_BAD_REQUEST)

class event_type_details(APIView):
    
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]


    def get(self, *args, **kwargs):
        eventType = get_object_or_404(
            EventType, uuid=self.kwargs['uuid'], deleted_status=False)
        acctype_serializer = EventTypeSerializer(eventType)
        return JsonResponse(acctype_serializer.data, safe=False, status=status.HTTP_200_OK)


    def put(self,*args, **kwargs):
        try:
            eventType = get_object_or_404(
                EventType, uuid=self.kwargs['uuid'], deleted_status=False)
            eventType.name=self.request.data['name']
            eventType.description=self.request.data['description']
            eventType.save()
            return JsonResponse(data=EventTypeSerializer(eventType).data, safe=False, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse(data=e, safe=False, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, *args, **kwargs):
        try:
            eventType = get_object_or_404(
                EventType, uuid=self.kwargs['uuid'], deleted_status=False)
            eventType.deleted_status = True
            eventType.save()
            return JsonResponse(data="Event Type Deleted successfuly", safe=False,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse(data="Internal Server Error", safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
