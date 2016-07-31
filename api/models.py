from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from customUser.models import MyUser

class Food(models.Model):
    """
    Food model, have M2M relation with Event.
    """
    title = models.CharField(max_length=50)
    img = models.ImageField()


class Event(models.Model):
    """
    Event model, contains all information about event and relationships to
    User model for host of event.
    """
    user = models.ForeignKey(MyUser, related_name='events')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    numOfPeople = models.IntegerField()
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    price = models.FloatField(blank=True, default=0.0)

    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(null=True)

    is_public = models.NullBooleanField()

    # Participant relationship
    participant = models.ManyToManyField('customUser.MyUser',
                                         related_name="participants",
                                         through="ParticipantsInEvent")

    # Food relationship
    food = models.ManyToManyField(Food, null=True, blank=True)
    
    # Geo Django location data
    objects = models.Manager()
    location = models.PointField(max_length=40, null=True)
    #distance = models.FloatField(null=True)
    geo_objects = models.GeoManager()

    class Meta:
        ordering = ['-date_created']

    def __unicode__(self):
        return self.title

    #
    # Class methods
    #
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.date_updated = timezone.now()
        super(Event, self).save(*args, **kwargs)


class ParticipantsInEvent(models.Model):
    """
    ManyToMany Relation for participants in an event
    """
    event = models.ForeignKey('api.Event', related_name="participatingEvent")
    user = models.ForeignKey('customUser.MyUser', related_name="participatingUser")
    date_joined = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    extra_friends = models.IntegerField(null=True)

    def __unicode__(self):
        return "%s is attending event %s" % (self.user.first_name, self.event)
