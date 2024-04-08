from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from django.contrib.auth.models import Permission
from rest_framework import status
import requests
from accounts.serializers.userSerializer import UserSerializer
from accounts.serializers.permissionSerializer import PermissionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from event.models.package import Package
from event.models.activity import Activity
from event.serializers import PackageActivitySerializer,PackageSerializer,ActivitySerializer
from  datetime import datetime




class activity_list(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]
    # permissions = ['admin.add_logentry']

    def get(self, *args, **kwargs):
            activities = Activity.all()
            serializer = ActivitySerializer(activities, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,*args, **kwargs):
        try:
            activity=Activity()
            activity.name=self.request.data['name']
            activity.save()
            
            return JsonResponse(data=ActivitySerializer(activity).data, safe=False, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return JsonResponse(data=e, safe=False, status=status.HTTP_400_BAD_REQUEST)

class activity_details(APIView):
    
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]


    def get(self, *args, **kwargs):
        activity = get_object_or_404(
            Activity, uuid=self.kwargs['uuid'], deleted_status=False)
        activity_serializer = ActivitySerializer(activity)
        return JsonResponse(activity_serializer.data, safe=False, status=status.HTTP_200_OK)


    def put(self,*args, **kwargs):
        try:
            activity = get_object_or_404(
                Activity, uuid=self.kwargs['uuid'], deleted_status=False)
            activity.name=self.request.data['name']
            activity.save()
            return JsonResponse(data=ActivitySerializer(activity).data, safe=False, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse(data=e, safe=False, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, *args, **kwargs):
        try:
            activity = get_object_or_404(
                Activity, uuid=self.kwargs['uuid'], deleted_status=False)
            activity.deleted_status = True
            activity.save()
            return JsonResponse(data="Activity Type Deleted successfuly", safe=False,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse(data="Internal Server Error", safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
