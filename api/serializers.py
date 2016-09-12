__author__ = 'jacob'

# imports
from customUser.models import MyUser
from rest_framework import serializers
from .models import Event, ParticipantsInEvent, Food

from django.contrib.gis.geos import fromstr, GEOSGeometry

from drf_extra_fields.geo_fields import PointField
from drf_extra_fields.fields import Base64ImageField


class SignUpSerializer(serializers.ModelSerializer):

	#profile_picture = Base64ImageField(required=False)
	profile_picture = serializers.ImageField(max_length=None)
	class Meta:
		model = MyUser
		fields = ('email', 'first_name', 'date_of_birth', 'password', 'profile_picture')
		write_only_fields = ('password',)
	
	"""
	def create(self, validated_data):
		user = MyUser.objects.create_user(
			email=validated_data['email'],
			date_of_birth=validated_data['date_of_birth'],
			first_name=validated_data['first_name'],
			password=validated_data['password'],
		)

		user.save()

		return user
	"""


class UserSerializer(serializers.ModelSerializer):
	events = serializers.PrimaryKeyRelatedField(many=True, queryset=Event.geo_objects.all())

	class Meta:
		model = MyUser
		fields = ('pk', 'email', 'events', 'date_of_birth', 'first_name', 'profile_picture')
		write_only_fields = ('password')
		
	def create(self, validated_data):
		user = MyUser.objects.create_user(
			email=validated_data['email'],
			date_of_birth=validated_data['date_of_birth'],
			first_name=validated_data['first_name'],
			password=validated_data['password'],
			profile_picture=validated_data['profile_picture']
		)

		user.set_password(validated_data['password'])
		user.save()

		return user
		
		
class EventParticipantSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ParticipantsInEvent
		fields = ('date_joined', 'is_accepted','user', 'event')


class EventSerializer(serializers.ModelSerializer):
	participant = UserSerializer(many=True)
	class Meta:
		model = Event
		fields = ('pk', 'user', 'title', 'description', 'numOfPeople',
				  'date_start', 'date_end', 'date_created',
				  'date_updated', 'is_public', 'location',
				  'food', 'participant', 'price',
				  )
	
	def to_representation(self, instance):
		ret = super(EventSerializer, self).to_representation(instance)
		pnt = fromstr(ret['location'])
		ret['location'] = {'longitude': pnt.coords[0], 'latitude': pnt.coords[1]}
		ret['distance'] = instance.distance.km
		return ret


class EventCreateSerializer(serializers.ModelSerializer):
	location = PointField(required=False)
	
	class Meta:
		model = Event
		fields = ('pk', 'user', 'title', 'description', 'numOfPeople',
				  'date_start', 'date_end', 'date_created',
				  'date_updated', 'is_public', 'location',
				  'food', 'participant',
				  )
