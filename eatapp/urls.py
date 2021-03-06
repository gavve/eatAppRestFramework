"""eatapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from api.views import *
from api import views as v

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

	url(r'^admin/', admin.site.urls),
	url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^events/$', EventList.as_view(), name='event-list'),
	url(r'^create_event/$', EventCreate.as_view(), name='event-create'),
	url(r'^update_participant/$',EventParticipantUpdate.as_view(), name='eventparticipant-update'),
	url(r'^events/(?P<pk>[0-9]+)/$', EventDetail.as_view(), name='event-detail'),
	url(r'^users/$', UserViewSet.as_view({'get': 'list'}), name='myuser-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='myuser-detail'),
	# url(r'^api/hello', ApiEndpoint.as_view()),  # and also a resource server!
	url(r'^sign_up/$', SignUp.as_view(), name="sign_up"),
	url(r'^upload/(?P<filename>[^/]+)/(?P<user_pk>[0-9]+)/$', FileUploadView.as_view()), # support for dealing with uploading profile_pictures
	url(r'^u_pk/(?P<pk>[0-9]+)/$', GetUserByPk.as_view(), name='getuserbypk-detail'),
	url(r'^u/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})', GetUserByMail.as_view(), name="getuserbymail-detail"),
	url(r'^device/gcm/?$', GCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_apns_device'),
]


#urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""url(r'^find_close_events/(?P<email_of_x>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<current_latitude>-?\d{2,3}.\d{5})/(?P<current_longitiude>-?\d{2,3}.\d{5})/$', v.find_close_events, name='event-list-local'),"""
