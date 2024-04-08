from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from Event_master.metadata import MetaData
from encrypted_id.models import EncryptedIDModel
import uuid
import datetime
import threading
from Event_master.utils.email_utils import EmailThread
from Event_master.settings import FRONTEND_PROJECT_URL
from user_management.models.client import Client
from rest_framework import serializers
 


class EmailSetPasswordThread(threading.Thread):

    def __init__(self, user, emp_name):
        self.user = user
        self.emp_name = emp_name
        threading.Thread.__init__(self)

    def run(self):
        self.user.send_password_set_email(
            self.user.ekey, self.emp_name, self.user.username)

    def join(self, timeout=None):
        """ Stopping the thread. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)


class ForgotEmailThread(threading.Thread):

    def __init__(self, user, emp_name):
        self.user = user
        self.emp_name = emp_name
        threading.Thread.__init__(self)

    def run(self):
        self.user.send_forgot_password_set_email(
            self.user.ekey, self.emp_name, self.user.username)

    def join(self, timeout=None):
        """ Stopping the thread. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)


class VerifyEmailThread(threading.Thread):

    def __init__(self, user, emp_name):
        self.user = user
        self.emp_name = emp_name
        threading.Thread.__init__(self)

    def run(self):
        self.user.send_email_verification(
            self.user.ekey, self.emp_name, self.user.username)

    def join(self, timeout=None):
        """ Stopping the thread. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)




def wrapper(instance, filename):
    new_filename = str(datetime.datetime.now()).split(
        '.')[0]+'_'+str(instance.id).split('-')[0]+'__'+filename
    return 'profilePictures/'+new_filename


# Create your models here.
class User(AbstractUser, MetaData, EncryptedIDModel):
    is_new = models.BooleanField(default=False)
    role = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=False, unique=True, null=False)
    referenceName = models.CharField(max_length=255, blank=True, null=True)
    referenceId = models.IntegerField(blank=True, null=True)
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, blank=False, null=False)
    has_reset_password = models.BooleanField(default=False)
    gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female'), (
        'Prefer not to say', 'Prefer not to say')], default='Prefer not to say')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=wrapper, null=True, default=None)
    has_set_password = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_client=models.BooleanField(default=False)
    is_organizer=models.BooleanField(default=False)
    latest_Profile=models.CharField(blank=True,null=True)

    USERNAME_FIELD = "username"

    class Meta:
        db_table = "users"

         
    @staticmethod
    def send_password_set_email(id, name, email):
        html_content = f'<h3>Dear {name}</h3>'
        html_content += f'<p>Welcome , you\'ve been registered to use the ACCOUNTING MASTER system, kindly follow this link to set your password</p>'
        html_content += f'<p>your <strong>username</strong> will be {email}</p>'
        html_content += f'<p>click <a href="{FRONTEND_PROJECT_URL}/set_password?tkn={id}">here</a> to set your password</p>'
        html_content += f'<p>Or copy and paste this link in the browser: {FRONTEND_PROJECT_URL}/set_password?tkn={id}</p>'
        EmailThread('HTML', 'Welcome to ACCOUNTING MASTER SYSTEM',
                    html_content, email).start()

    @staticmethod
    def send_forgot_password_set_email(id, name, email):
        html_content = f'<h3>Dear {name}</h3>'
        html_content += f'<p>kindly follow this link to Reset your password</p>'
        html_content += f'<p>your <strong>username</strong> will be {email}</p>'
        html_content += f'<p>click <a href="{FRONTEND_PROJECT_URL}/set_password?tkn={id}">here</a> to Reset your password</p>'
        html_content += f'<p>Or copy and paste this link in the browser: {FRONTEND_PROJECT_URL}/set_password?tkn={id}</p>'
        EmailThread('HTML', 'PASSWORD RESET - ACCOUNTING MASTER SYSTEM',
                    html_content, email).start()

    @staticmethod
    def send_email_verification(id, name, email):
        html_content = f'<h3>Dear {name}</h3>'
        html_content += f'<p>kindly follow this link to verify your email</p>'
        html_content += f'<p>your <strong>username</strong> will be {email}</p>'
        html_content += f'<p>click <a href="{FRONTEND_PROJECT_URL}/verify_email?tkn={id}">here</a> to Verify your email</p>'
        html_content += f'<p>Or copy and paste this link in the browser: {FRONTEND_PROJECT_URL}/verify_email?tkn={id}</p>'
        EmailThread('HTML', 'VERIFY EMAIL - ACCOUNTING MASTER SYSTEM',
                    html_content, email).start()



class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    # date_of_birth = serializers.DateField(required=False)
    # address = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.CharField(read_only=True)
    uuid = serializers.UUIDField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_active=serializers.BooleanField(read_only=True)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email',
                  'phone_number', 'is_email_verified', 'profile_picture', 'password', 'is_new','is_admin','is_active','role','uuid', 'is_superuser']

    def get_instance(self):
        user = User()

        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.username = self.validated_data['username']
        user.email = self.validated_data['username']
        # user.gender = self.validated_data['gender']
        user.phone_number = self.validated_data['phone_number']
        # if 'date_of_birth' in self.validated_data:
        #     user.date_of_birth = self.validated_data['date_of_birth']
        # if 'address' in self.validated_data:
        #     user.address = self.validated_data['address']
        if 'profile_picture' in self.validated_data:
            user.profile_picture = self.validated_data['profile_picture']

        if 'password' in self.validated_data:
            user.set_password(self.validated_data['password'])

        return user

    def save(self):
        user = self.get_instance()
        user.save()
        if len(user.password) == 0:
            user.send_password_set_email(
            user.ekey, self.emp_name, self.user.username)
        return user
 

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email',
                  'date_of_birth', 'address', 'phone_number', 'uuid']


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()
