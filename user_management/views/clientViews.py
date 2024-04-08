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
from user_management.serializers.serializer import ClientSerializer,RegistrationSerializer,ProfileSerializer
from accounts.models import User
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from  datetime import datetime
 
from user_management.models.client import Client
from user_management.models.digital_profile import DigitalProfile
from user_management.models.role import Role
 
import time
 

class client_list(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, *args, **kwargs):
        clients = Client.all_clients()
        serializer = ClientSerializer(clients, many=True)
        return JsonResponse(serializer.data, safe=False)

class registerInstitution(APIView):

    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]

    def post(self,*args , **kwargs):
        serializer = RegistrationSerializer(
            data=self.request.data)
        if serializer.is_valid():
            if self.request.POST.get('is_organizer')==True:
                client = serializer.create()
                return JsonResponse(data=ClientSerializer(client).data, safe=False, status=status.HTTP_201_CREATED)
            else:
                organizer = serializer.create()
                return JsonResponse(data=ClientSerializer(organizer).data, safe=False, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)


class beOrganizer(APIView):

    
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]

    def post(self,*args , **kwargs):
        
        client = get_object_or_404(
            Client, uuid=self.kwargs['uuid'], deleted_status=False)

        existingProfile=DigitalProfile.objects.get(referenceId=client.pk,deleted_status=False,referenceName='Client')
        if not existingProfile is None:
            oProfile=DigitalProfile.objects.get(referenceId=client.pk,deleted_status=False,referenceName='Organizer')
            if oProfile is None:
                dprofile=DigitalProfile()
                dprofile.referenceId=client.pk
                dprofile.referenceName='Organizer'
                dprofile.role=Role.objects.get(pk=1)
                dprofile.user=existingProfile.user
                dprofile.save()

                return JsonResponse(data=ProfileSerializer(dprofile).data, safe=False, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse("You Are Already an Organizer", safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse("You Need First to be Client of Application", safe=False, status=status.HTTP_400_BAD_REQUEST)
 
        


    