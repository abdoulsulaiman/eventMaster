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
from event.models.package_activity import PackageActivity
from event.serializers import PackageActivitySerializer,PackageSerializer,ActivitySerializer
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from  datetime import datetime




class package_list(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]
    # permissions = ['admin.add_logentry']

    def get(self, *args, **kwargs):
            packages = Package.all()
            serializer = PackageSerializer(packages, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,*args, **kwargs):
        try:
            package=Package()
            package.name=self.request.data['name']
            package.save()
            
            return JsonResponse(data=PackageSerializer(package).data, safe=False, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return JsonResponse(data=e, safe=False, status=status.HTTP_400_BAD_REQUEST)

class package_details(APIView):
    
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]


    def get(self, *args, **kwargs):
        package = get_object_or_404(
            Package, uuid=self.kwargs['uuid'], deleted_status=False)
        acctype_serializer = PackageSerializer(package)
        return JsonResponse(acctype_serializer.data, safe=False, status=status.HTTP_200_OK)


    def put(self,*args, **kwargs):
        try:
            package = get_object_or_404(
                Package, uuid=self.kwargs['uuid'], deleted_status=False)
            package.name=self.request.data['name']
            package.save()
            return JsonResponse(data=PackageSerializer(package).data, safe=False, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse(data=e, safe=False, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, *args, **kwargs):
        try:
            package = get_object_or_404(
                Package, uuid=self.kwargs['uuid'], deleted_status=False)
            package.deleted_status = True
            package.save()
            return JsonResponse(data="Package Type Deleted successfuly", safe=False,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse(data="Internal Server Error", safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetPackageActivities(APIView):
 
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny]


    def get(self, *args, **kwargs):
        try: 
 
            # Assuming package_id is the primary key of the Package model
            package_activities =PackageActivity.objects.filter(package=self.kwargs['pk'])
            # Retrieve the activity objects associated with the package_activities queryset
            activities = [package_activity.activity for package_activity in package_activities]
            
            serializer = ActivitySerializer(activities, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
             return JsonResponse(data=e, safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
