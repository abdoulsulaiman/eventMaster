from rest_framework import serializers
from accounts.models import User
from accounts.serializers.permissionSerializer import PermissionSerializer
from accounts.serializers.groupSerializer import GroupSerializer


class UserSerializer(serializers.ModelSerializer):
    # user_permissions = PermissionSerializer(many=True)
    # groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name','phone_number','username','has_set_password','has_reset_password','email','latest_Profile')

    def get_instance(self):
        user = User()
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.username = self.validated_data['username']
        user.email = self.validated_data['username']

        return user

    def save(self):
        user = self.get_instance()
        user.save()
        return user


class UserUpdateSerializer(serializers.Serializer):
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    address=serializers.CharField(required=False)
    gender=serializers.CharField(required=False)
    date_of_birth=serializers.CharField(required=False)
    email=serializers.CharField(required=True)
    phone_number=serializers.CharField(required=True)

    def update(self,user):
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        if 'address' in self.validated_data:
            user.address = self.validated_data['address']
        if 'gender' in self.validated_data:
            user.gender = self.validated_data['gender']
        if 'date_of_birth' in self.validated_data:
            user.date_of_birth=self.validated_data['date_of_birth']
        user.phone_number=self.validated_data['phone_number']
        user.email=self.validated_data['email']
        user.save()
        return user

