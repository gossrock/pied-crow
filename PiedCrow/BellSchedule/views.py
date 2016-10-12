from django.shortcuts import render, get_object_or_404, get_list_or_404

# Create your views here.
from django.http import HttpResponse

from time import time


from .models import Schedule, BellRing



def index(request):
	context = {}
	return render(request, 'BellSchedule/index.html', context)


def clock_js(request):
	context = {'server_load_time': (time() * 1000)}
	return render(request, 'BellSchedule/js/clock.js', context)

def bell_times_xml(request):
	sched = get_object_or_404(Schedule, name='Default')
	context = {'schedule':sched}
	return render(request, 'BellSchedule/data/bell_times.xml', context, content_type='application/xml')
