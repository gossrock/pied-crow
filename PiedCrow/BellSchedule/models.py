from django.db import models

from datetime import date
from datetime import timedelta as td


# Create your models here.
class Schedule (models.Model):
	name = models.CharField("Schedule Name",max_length=30)
	
	def __str__(self):
		return self.name

class RingPattern (models.Model):
	name = models.CharField("Ring Pattern Name", max_length=30)
	repeat = models.BooleanField("Pattern Repeats")
	
	def __str__(self):
		return self.name
	
class RingPatternPart (models.Model):
	ring_pattern = models.ForeignKey(RingPattern, on_delete=models.CASCADE)
	on_off = models.BooleanField("On")
	duration = models.FloatField("Duration of Part")

class BellRing (models.Model):
	schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
	time = models.TimeField("Ring Time")
	ring_pattern = models.ForeignKey(RingPattern)
	note = models.CharField("Note", max_length=200)
	
	def hour(self):
		return self.time.hour

	def minute(self):
		return self.time.minute	


############################

class YearCalendar(models.Model):
	name = models.CharField("Schedule Name",max_length=50)
	start_date = models.DateField()
	end_date = models.DateField()
	sun_off = models.BooleanField("Sunday Off", default=True) # = 7
	mon_off = models.BooleanField("Monday Off", default=False) # = 0
	tue_off = models.BooleanField("Tuesday Off", default=False) # = 1
	wed_off = models.BooleanField("Wednesday Off", default=False) # = 2
	thr_off = models.BooleanField("Thursday Off", default=False) # = 3
	fri_off = models.BooleanField("Friday Off", default=False) # = 4
	sat_off = models.BooleanField("Saturday Off", default=True) # = 5
	
	def __str__(self):
		return self.name
	
	def todays_schedule(self):
		return self.years_schedules()[date.today()]
		
		
	def years_schedules(self):
		day_schedules = {}
		start_day = self.start_date
		end_day = self.end_date
		day = start_day
		while (day <= end_day): # fill the dictionary with the day keys
			day_schedules[day] = None
			day = day + td(days=1)
			
		# fill in special day schedules
		special_days = self.specialday_set.all()
		for day in special_days:
			day_schedules[day.date] = day.schedule
			
		# fill in other schedules
		week_days_off = [self.mon_off, self.tue_off, self.wed_off, self.thr_off, self.fri_off, self.sat_off, self.sun_off]
		normal_rotation = self.normalschedulerotation_set.all()
		rot_num = len(normal_rotation)
		i = 0
		day = start_day
		while day <= end_day:
			off = week_days_off[day.weekday()]
			if off:
				pass
			elif day_schedules[day] is not None:
				special = self.specialday_set.get(date=day)
				if special.keep_normal_rotation:
					i += 1
			else:
				sched = normal_rotation[i % rot_num].schedule
				day_schedules[day] = sched
				i += 1
			day = day + td(days=1)
		return day_schedules
		
def get_current_calendar():
	calendars = YearCalendar.objects.all()
	for cal in calendars:
		today = date.today()
		if today >= cal.start_date and today <=cal.end_date:
			return cal
			
class NormalScheduleRotation(models.Model):
	year_calendar = models.ForeignKey(YearCalendar, on_delete=models.CASCADE)
	order = models.IntegerField()
	schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)			

class SpecialDay(models.Model):
	name = models.CharField("Name",max_length=50)
	year_calendar = models.ForeignKey(YearCalendar, on_delete=models.CASCADE)
	date = models.DateField()
	schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
	keep_normal_rotation = models.BooleanField("Keep Normal Rotation", default=False)	
	
#################################################

class EmergencyType(models.Model):
	name = models.CharField("Emergency Type Name", max_length=30)
	ring_pattern = models.ForeignKey(RingPattern, related_name='ring_pattern', null=True, on_delete=models.SET_NULL)
	all_clear_pattern = models.ForeignKey(RingPattern, related_name='all_clear_pattern', null=True, on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.name
		
class EmergencyEvent(models.Model):
	emergency_type = models.ForeignKey(EmergencyType, on_delete=models.PROTECT)
	start_time = models.DateTimeField(default=None, null=True, blank=True)
	stop_time = models.DateTimeField(default=None, null=True, blank=True)
	all_clear_time = models.DateTimeField(default=None, null=True, blank=True)
	

	
def get_current_emergency_events():
	return EmergencyEvent.objects.filter(start_time__isnull=False, all_clear_time__isnull=True)


def get_todays_emergency_events():
	today = date.today()
	y = today.year
	m = today.month
	d = today.day
	return EmergencyEvent.objects.filter(start_time__year=y, start_time__month=m, start_time__day=d)
