from rest_framework import serializers
from datetime import datetime ,timedelta
from django.shortcuts import get_object_or_404
from event.models.activity import Activity
from event.models.package import Package
from event.models.package_activity import PackageActivity
from event.models.event import Event
from event.models.event_type import EventType
import decimal

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Activity
        fields='__all__'

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Package
        fields='__all__'

class PackageActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model=PackageActivity
        fields='__all__'

    def to_representation(self, instance):
        self.fields['package'] = PackageSerializer(read_only=True)
        return super(PackageActivitySerializer, self).to_representation(instance)
    
    def get_activity(self, instance):
        self.fields['activity'] = ActivitySerializer(read_only=True)
        return super(PackageActivitySerializer, self).to_representation(instance)


class CreatePackageActivitySerializer(serializers.Serializer):
    package_id = serializers.CharField(max_length=200)
    activity_id = serializers.CharField(max_length=1000)
    
    def create(self):
                package_activity=PackageActivity()
                package_activity.package=Package.objects.get(pk=self.validated_data.pop('package_id'))
                package_activity.activity=Activity.objects.get(pk=self.validated_data.pop('activity_id'))
                package_activity.save()
                return package_activity
    

class CreateEventSerializer(serializers.Serializer):
    package_id = serializers.CharField(max_length=200)
    event_name=serializers.CharField(max_length=200)
    can_sell_ticket=serializers.BooleanField()
    isPayableEvent=serializers.BooleanField()
    landingImage = serializers.ImageField()
    homeImage=serializers.ImageField()
    eventCategory=serializers.CharField(max_length=200)
    type_id=serializers.CharField(max_length=200)

    def create(self,client_id):
         event=Event()
         event.package=Package.objects.get(pk=self.validated_data.pop('package_id'))
         event.type=EventType.objects.get(pk=self.validated_data.pop('type_id'))
         event.name=self.validated_data.pop("event_name")
         event.isPayableEvent=self.validated_data.pop("isPayableEvent")
         event.landingImage=self.validated_data.pop("landingImage")
         event.homeImage=self.validated_data.pop("homeImage")
         event.eventCategory=self.validated_data.pop("eventCategory")
         event.referenceId=client_id
         event.save()
         return event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields='__all__'

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=EventType
        fields='__all__'
