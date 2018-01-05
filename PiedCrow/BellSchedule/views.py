from django.shortcuts import render, get_object_or_404, get_list_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from time import time
from datetime import datetime
from django.contrib.auth.decorators import login_required


from .models import Schedule, BellRing, YearCalendar, get_current_calendar
from .models import EmergencyType, EmergencyEvent, get_current_emergency_events, get_todays_emergency_events



def index(request):
	context = {}
	return render(request, 'BellSchedule/index.html', context)


def clock_js(request):
	context = {'server_load_time': (time() * 1000)}
	return render(request, 'BellSchedule/js/clock.js', context)
	
def server_time_text(request):
	context = {'server_time': (time() * 1000)}
	return render(request, 'BellSchedule/data/server_time', context, content_type='application/text')

def bell_times_xml(request):
	sched = YearCalendar.objects.all()[0].todays_schedule()
	context = {'schedule':sched}
	return render(request, 'BellSchedule/data/bell_times.xml', context, content_type='application/xml')
	
def view_schedule(request, sched_id):
	sched = get_object_or_404(Schedule, pk=sched_id)
	return render(request, "BellSchedule/schedule.html", {'schedule': sched})

def calendar (request, cal_id):
	cal = get_object_or_404(YearCalendar, pk=cal_id)
	return render(request, "BellSchedule/calendar.html", {'calendar': cal, 'days': sorted(cal.years_schedules().items())})

def current_calendar (request):
	cal = get_current_calendar()
	return render(request, "BellSchedule/calendar.html", {'calendar': cal, 'days': sorted(cal.years_schedules().items())})

@login_required
def view_alarms(request):
	types = EmergencyType.objects.all()
	all_events = EmergencyEvent.objects.all()
	events_today = get_todays_emergency_events()
	current_events = get_current_emergency_events()
	context = {'types': types, 'all_events': all_events, 'te':events_today, 'current_events':current_events}
	return render(request, 'BellSchedule/alarms.html', context)

@login_required
def start_alarm(request, emergency_type_id):
	em_type = EmergencyType.objects.get(pk=emergency_type_id)
	now = datetime.today()
	em_type.emergencyevent_set.create(start_time=now)
	
	return HttpResponseRedirect('/alarms/')
	
	
@login_required
def stop_alarm(request, emergency_event_id):
	em_event = EmergencyEvent.objects.get(pk=emergency_event_id)
	now = datetime.today()
	em_event.stop_time = now
	em_event.save()
	
	return HttpResponseRedirect('/alarms/')

@login_required
def all_clear_alarm(request, emergency_event_id):
	em_event = EmergencyEvent.objects.get(pk=emergency_event_id)
	now = datetime.today()
	if em_event.stop_time is None:
		em_event.stop_time = now
	em_event.all_clear_time = now
	em_event.save()
	
	return HttpResponseRedirect('/alarms/')
