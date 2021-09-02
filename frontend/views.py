from django.shortcuts import render
from .models import Destination

def index(request):
	# dest1 = Destination()
	# dest1.name = 'Mumbai'
	# dest1.desc = 'Beautiful City'
	# dest1.img = 'destination_3.jpg'
	# dest1.price = 700
	# dest1.offer = True

	# dest2 = Destination()
	# dest2.name = 'Mumbai'
	# dest2.desc = 'Beautiful City'
	# dest2.img = 'destination_3.jpg'
	# dest2.price = 700
	# dest2.offer = False

	# dests = [dest1,dest2]

	dests = Destination.objects.all()
	
	return render(request, "frontend.html", {'dests': dests})
