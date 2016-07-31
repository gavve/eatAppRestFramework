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
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, permissions, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes


from api.serializers import UserSerializer, EventSerializer, SignUpSerializer, EventSerializer, EventCreateSerializer, EventParticipantSerializer
from api.models import Event, ParticipantsInEvent, Food
from customUser.models import MyUser


from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from oauth2_provider.decorators import protected_resource



class SignUp(generics.CreateAPIView):
	queryset = MyUser.objects.all()
	serializer_class = SignUpSerializer
	permission_classes = (IsAuthenticatedOrCreate,)


class ApiEndpoint(ProtectedResourceView):
	def get(self, request, *args, **kwargs):
		return HttpResponse('Hello, OAuth2!')


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
