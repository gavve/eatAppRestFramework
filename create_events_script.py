from api.models import Event
from customUser.models import MyUser
import random
from django.contrib.gis.geos import GEOSGeometry



def run():
	y = 0

	while y < 100:
		longitude = random.uniform(17.0, 18.0)
		lat = random.uniform(60.0, 61.0)
		A = GEOSGeometry('POINT('+str(longitude)+' ' + str(lat)+')', srid=4326)
		e = Event(user=MyUser.objects.get(pk=1), title="Lunch", description="En riktigt god lunch utlovas, kyckling och potatis. Kommer endast att kosta runt 30 kr.",
				 numOfPeople=random.randint(3,12), date_start="2016-07-"+str(random.randint(1,18)) +" 13:00:00.00Z", price=3, location=A)
		e.save()
		print y
		y += 1
		
def delete():
	e=Event.objects.filter(title="Lunch", price=3)
	a = 0
	for i in e:
		print a
		i.delete()
		a += 1
run()
