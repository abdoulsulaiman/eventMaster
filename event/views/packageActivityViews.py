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
from event.models.package import Package
from event.models.activity import Activity
from event.serializers import PackageActivitySerializer,PackageSerializer,ActivitySerializer,CreatePackageActivitySerializer
from  datetime import datetime



class addPackageActity(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]
    # permissions = ['admin.add_logentry']

    def post(self,*args, **kwargs):
        serializer = CreatePackageActivitySerializer(
            data=self.request.data)
        if serializer.is_valid():
            activity = serializer.create()
            return Response(data=PackageActivitySerializer(activity).data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

