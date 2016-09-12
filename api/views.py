# Imports
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.auth.decorators import login_required
from django.test.client import RequestFactory

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FileUploadParser, FormParser, MultiPartParser
from rest_framework import viewsets, permissions, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, parser_classes


from api.serializers import *
from api.models import Event, ParticipantsInEvent, Food
from customUser.models import MyUser


from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from oauth2_provider.decorators import protected_resource

import StringIO

import base64
import os
from django.core.files import File 
from django.core.files.base import ContentFile
from PIL import Image


class SignUp(generics.CreateAPIView):
	queryset = MyUser.objects.all()
	serializer_class = SignUpSerializer
	permission_classes = (IsAuthenticatedOrCreate,)
	parser_classes = (MultiPartParser, FormParser)

	def post(self, request, format=None):
		serializer = SignUpSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadView(APIView):
	parser_classes = (FileUploadParser,)

	def put(self, request, filename, user_pk, format=None):
		file_obj = request.data['file']
		#f=open('profilepictures/donalduploaded.jpg')
		#f.write(file_obj,'wb')
		#f.close()
		# Save file (image) to user
		# image_file = StringIO.StringIO(file_obj.read()) 
		user = MyUser.objects.get(pk=user_pk)
		#user.profile_picture.save('profilepictures/'+str(user.pk)+'.jpg', ContentFile(im))
		from PIL import Image as ImageObj
		from cStringIO import StringIO
		from django.core.files.uploadedfile import SimpleUploadedFile

		try:
			# thumbnail
			THUMBNAIL_SIZE = (160, 160)  # dimensions

			image = ImageObj.open(file_obj)

			# Convert to RGB if necessary
			if image.mode not in ('L', 'RGB'): image = image.convert('RGB')

			# create a thumbnail + use antialiasing for a smoother thumbnail
			#image.thumbnail(THUMBNAIL_SIZE, ImageObj.ANTIALIAS)

			# fetch image into memory
			temp_handle = StringIO()
			user.profile_picture.save(temp_handle, 'png')
			temp_handle.seek(0)

			# save it
			#file_name, file_ext = os.path.splitext(self.image.name.rpartition('/')[-1])
			suf = SimpleUploadedFile("file_name" + file_ext, temp_handle.read(), content_type='image/png')

			#self.thumbnail.save(file_name + '.png', suf, save=False)
		except ImportError:
			pass
		return Response(status=204)


class UserViewSet(viewsets.ModelViewSet):
	"""
	A viewset for viewing and editing user instances.
	"""
	serializer_class = UserSerializer
	queryset = MyUser.objects.all()


class UserDetail(generics.RetrieveAPIView):
	queryset = MyUser.objects.all()
	serializer_class = UserSerializer


class GetUserByPk(generics.RetrieveAPIView):
	queryset = MyUser.objects.all()
	serializer_class = UserSerializer
	lookup_field = "pk"
	
class GetUserByMail(generics.RetrieveAPIView):
	queryset = MyUser.objects.all()
	serializer_class = UserSerializer
	lookup_field = "email"


class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


class EventList(generics.ListAPIView):
	"""
	List all events, or create a new event.
	"""
	serializer_class = EventSerializer
	renderer_class = JSONRenderer

	def get_queryset(self):
		"""
		Optionally restricts the returned events to a given user,
		by filtering against a `email` query parameter in the URL.
		"""
		
		
		user_pk = self.request.query_params.get('pk', None)
		user = get_object_or_404(MyUser, pk=user_pk)
		current_latitude = self.request.query_params.get('lat', None)
		current_longitude = self.request.query_params.get('long', None)
		queryset = find_close_events(user, current_latitude, current_longitude)
		return queryset


class EventCreate(generics.CreateAPIView):
	"""
	For creating an event
	"""
	serializer_class = EventCreateSerializer
	renderer_class = JSONRenderer
	
	
	
class EventParticipantUpdate(generics.CreateAPIView):
	"""
	Update Event with a new Participant
	"""
	model = ParticipantsInEvent
	serializer_class = EventParticipantSerializer
	queryset = ParticipantsInEvent.objects.all()


class EventDetail(APIView):
	"""
	Retrieve, update or delete an event instance.
	"""
	permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope,)

	def get_object(self, pk):
		try:
			return Event.objects.get(pk=pk)
		except Event.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		event = self.get_object(pk)
		serializer = EventSerializer(event)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		event = self.get_object(pk)
		serializer = EventSerializer(event, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		event = self.get_object(pk)
		event.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)



def find_close_events(user, current_latitude, current_longitiude, limit=10):

	finder = get_object_or_404(MyUser, pk=user.pk)
	finder_location = Point(float(current_longitiude), float(current_latitude))

	
	events = Event.geo_objects.all()

	# do geo queries
	events_within_user_radius = events.filter(
		location__distance_lte=(
			finder_location,
			D(km=min(user.prefered_radius, F('prefered_radius'))))
		).distance(finder_location).order_by('distance')[:limit]

	return events_within_user_radius
