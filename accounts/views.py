from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from oauth2_provider.contrib.rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from user_management.models.client import Client
from accounts.models import User, ForgotEmailThread, SetPasswordSerializer, ChangePasswordSerializer, VerifyEmailThread, UserSerializer
from encrypted_id import decode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from accounts.serializers.userSerializer import UserUpdateSerializer,UserSerializer

from user_management.models.digital_profile import DigitalProfile
from user_management.serializers.serializer import ProfileData,ProfileSerializer


 

class GetUserProfile(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        try:
            if self.request.user.latest_Profile is None:
                user=self.request.user
                user.latest_Profile='Client'
                user.save()

            client=Client.objects.get(pk=self.request.user.referenceId)    
            digitalProfileCount=DigitalProfile.objects.filter(user=self.request.user,referenceId=client.pk).count()
            has_more_profile=False
            if digitalProfileCount >1:
                has_more_profile=True
            profile=ProfileData()
            profile.pk=self.request.user.id
            profile.first_name=self.request.user.first_name
            profile.last_name=self.request.user.last_name
            profile.username=self.request.user.username
            profile.phone_number=client.phone
            profile.email=self.request.user.email
            profile.client=client
            profile.has_more_profile=has_more_profile

            return Response(data=ProfileSerializer(profile).data, status=status.HTTP_200_OK)
        except (User.DoesNotExist):
            return Response(data="We couldn't find the data associated to this user, kindly contact administrator!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SwitchUserProfile(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        try:
            if self.kwargs['profile_type']=="Client":
               print(self.request.user)
               profile=DigitalProfile.objects.get(user=self.request.user,deleted_status=False,referenceName='Client')
               if not profile is None:
                    profile_data =ProfileData()
                    profile_data.first_name=profile.user.first_name
                    profile_data.last_name=profile.user.last_name
                    profile_data.phone_number=profile.user.phone_number
                    profile_data.email=profile.user.email
                    profile_data.username=profile.user.username
                    profile_data.is_active=profile.user.is_active
                    profile_data.is_superuser=profile.user.is_superuser
                    profile_data.is_client=True
                    profile_data.client=Client.objects.get(pk=profile.referenceId,deleted_status=False)
                    # updating latest Profile in the DB
                    user=profile.user
                    user.latest_Profile="Client"
                    user.save()
                    return Response(data=ProfileSerializer(profile_data).data,status=status.HTTP_200_OK)
            else :
                profile=DigitalProfile.objects.get(user=self.request.user,deleted_status=False,referenceName='Organizer')
                if not profile is None:
                    profile_data =ProfileData()
                    profile_data.first_name=profile.user.first_name
                    profile_data.last_name=profile.user.last_name
                    profile_data.phone_number=profile.user.phone_number
                    profile_data.email=profile.user.email
                    profile_data.username=profile.user.username
                    profile_data.is_active=profile.user.is_active
                    profile_data.is_superuser=profile.user.is_superuser
                    profile_data.is_client=False
                    profile_data.client=None
                    profile_data.client=Client.objects.get(pk=profile.referenceId,deleted_status=False)
                    # updating latest Profile in the DB
                    user=profile.user
                    user.latest_Profile="Organizer"
                    user.save()
                    return Response(data=ProfileSerializer(profile_data).data, status=status.HTTP_200_OK)
        except (DigitalProfile.DoesNotExist):
            return Response(data="We couldn't find the data associated to this user, kindly contact administrator!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ChangePassword(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def put(self, *args, **kwargs):
        serialized_data = ChangePasswordSerializer(data=self.request.data)
        if serialized_data.is_valid():
            user = self.request.user
            if User.check_password(user, serialized_data.validated_data['old_password']):
                if serialized_data.validated_data['new_password1'] == serialized_data.validated_data['new_password2']:
                    user.set_password(
                        serialized_data.validated_data['new_password1'])
                    user.save()
                    return Response(data='Password successfully changed', status=status.HTTP_200_OK)
                return Response(data='New passwords don\'t match', status=status.HTTP_400_BAD_REQUEST)
            return Response(data='Invalid old Password', status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class set_password(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [AllowAny]

    def put(self, *args, **kwargs):
        token = self.kwargs['token']
        user = User.objects.get(pk=decode(token))
        # Check if User has set Password and Return Setting Password Link has Expired
        if user.has_set_password:
            return Response(data='The Link has Expired', status=status.HTTP_400_BAD_REQUEST)
        else:
            serialized_data = SetPasswordSerializer(data=self.request.data)
            if serialized_data.is_valid():
                if serialized_data.validated_data['password'] == serialized_data.validated_data['confirm_password']:
                    user.set_password(
                        serialized_data.validated_data['password'])
                    user.save()
                    return Response(data='Password is Set successfully ', status=status.HTTP_200_OK)
                return Response(data='Password and Confirm passwords don\'t match', status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

class reset_password(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [AllowAny]

    def put(self, *args, **kwargs):
        token = self.kwargs['token']
        user = User.objects.get(pk=decode(token))
        # Check if User has set Password and Return Setting Password Link has Expired
        if user.reset_password is False:
            return Response(data='The Link has Expired', status=status.HTTP_400_BAD_REQUEST)
        else:
            serialized_data = SetPasswordSerializer(data=self.request.data)
            if serialized_data.is_valid():
                if serialized_data.validated_data['password'] == serialized_data.validated_data['confirm_password']:
                    user.set_password(
                        serialized_data.validated_data['password'])
                    user.reset_password = False
                    user.save()
                    return Response(data='Password was  Reset successfully ', status=status.HTTP_200_OK)
                return Response(data='New Password and Confirm passwords don\'t match', status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
class ForgotPassword(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):
        email = self.request.data['email']
        user = User.objects.get(email=email)
        user.reset_password = True
        user.save()
        ForgotEmailThread(user, user.first_name).start()
        return Response(data=' Kindly Check your email for a link to reset your password', status=status.HTTP_200_OK)


class UpdateProfile(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def put(self, *args, **kwargs):
        user = get_object_or_404(
            User, uuid=self.kwargs['uuid'], deleted_status=False)

        user_serializer = UserUpdateSerializer(
            user, data=self.request.data)
        if user_serializer.is_valid():
            user1 = user_serializer.update(user)
            user1.last_updated_by = self.request.user.username
            user1.save()

            return JsonResponse(data=user_serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse(data=user_serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)


class verify_email(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [AllowAny]

    def put(self, *args, **kwargs):
        token = self.kwargs['token']
        user = User.objects.get(pk=decode(token))
        user.is_email_verified = True
        user.save()
        return Response(data='email  was verified successfully ', status=status.HTTP_200_OK)


class ResendVerificationEmail(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):
        email = self.request.data['email']
        user = User.objects.get(email=email)
        if not user is None:
            VerifyEmailThread(user, user.first_name).start()
            return Response(data=' Kindly Check your email for a link to Verify your email', status=status.HTTP_200_OK)
        else:
            return Response(data={'error': "User Not Found!"}, status=status.HTTP_404_NOT_FOUND)
