from django.test import TestCase
from api.models import Event, ParticipantsInEvent
from customUser.models import MyUser


class M2MThroughTest(TestCase):

    def setUp(self):
        # Create three people:
        self.joe = MyUser.objects.create(email='Joe@joe.se', password="test")
        self.jim = MyUser.objects.create(email='Jim@jim.se', password="test")
        self.bob = MyUser.objects.create(email='Bob@bob.se', password="test")

        # And three groups:
        self.dinner = Event.objects.create(user=self.jim, title='Dinner', description="test", numOfPeople=5)
        self.bbq = Event.objects.create(user=self.jim, title='BBQ', description="test", numOfPeople=5)
        self.lunch = Event.objects.create(user=self.bob, title='Lunch', description="test", numOfPeople=5)

        # Every user is a participant of different event
        ParticipantsInEvent.objects.create(user=self.joe, event=self.dinner)
        ParticipantsInEvent.objects.create(user=self.bob, event=self.bbq)
        ParticipantsInEvent.objects.create(user=self.bob, event=self.lunch)
        ParticipantsInEvent.objects.create(user=self.jim, event=self.lunch)
        ParticipantsInEvent.objects.create(user=self.jim, event=self.bbq)
        ParticipantsInEvent.objects.create(user=self.jim, event=self.dinner)

    def test_is_attending_hosted_event(self):
        # Is Bob attending his own event?
        bobs_event = Event.objects.filter(user=self.bob)
        self.assertEqual(list(bobs_event), [self.lunch])

    def test_participating_in_lunch(self):
        lunch_event = ParticipantsInEvent.objects.filter(event=self.lunch).values_list('user', flat=True)
        lunch_members = User.objects.filter(users__in=lunch_event)
        self.assertEqual(list(lunch_members), [self.jim, self.bob])