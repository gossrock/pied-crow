from django.db import models

# Create your models here.


class YearCalendar(models.Model):
	name = models.CharField("Schedule Name",max_length=50)
	start_date = models.DateField()
	end_date = models.DateField()
	sun_off = models.BooleanField("Sunday Off", default=True)
	mon_off = models.BooleanField("Monday Off", default=False)
	tue_off = models.BooleanField("Tuesday Off", default=False)
	wed_off = models.BooleanField("Wednesday Off", default=False)
	thr_off = models.BooleanField("Thursday Off", default=False)
	fri_off = models.BooleanField("Friday Off", default=False)
	sat_off = models.BooleanField("Saturday Off", default=True)
	
	def __str__(self):
		return self.name


class Schedule (models.Model):
	name = models.CharField("Schedule Name",max_length=30)
	
	def __str__(self):
		return self.name	
	
class SpecialDays(models.Model):
	name = models.CharField("Name",max_length=50)
	year_calendar = models.ForeignKey(YearCalendar, on_delete=models.CASCADE)
	date = models.DateField()
	schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
	keep_normal_rotation = models.BooleanField("Keep Normal Rotation", default=False)
	
class NormalScheduleRotation(models.Model):
	year_calendar = models.ForeignKey(YearCalendar, on_delete=models.CASCADE)
	order = models.IntegerField()
	schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)



		
		
class Bell (models.Model):
	name = models.CharField("Bell Name", max_length=30)
	gpio_pin = models.IntegerField("GPIO Pin Number")
	
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

class EmergencyBells(models.Model):
	name = models.CharField("Bell Name", max_length=30)
	ring_pattern = models.ForeignKey(RingPattern, on_delete=models.CASCADE)
	active = models.BooleanField(default=False)
	
	def __str__(self):
		return self.name
		
	def activate(self):
		self.active = True
		self.save()
		
	def deactivate(self):
		self.active = False
		self.save()
	
class EmergencyDrills (models.Model):
	name = models.CharField("Bell Name", max_length=30)
	emergency_bell = models.ForeignKey(EmergencyBells, on_delete=models.CASCADE)
	date = models.DateField()
	time = models.TimeField("Ring Time")
	
	def __str__(self):
		return self.name
	
	
