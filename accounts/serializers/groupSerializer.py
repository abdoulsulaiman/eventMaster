from rest_framework import serializers
from django.contrib.auth.models import Group, ContentType


class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer(read_only=True)

    class Meta:
        model = Group
        exclude = ['permissions']
