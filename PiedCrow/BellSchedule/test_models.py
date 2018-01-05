import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'PiedCrow.settings'
import django
django.setup()

from BellSchedule.models import YearCalendar
from datetime import timedelta as td
from datetime import date as date

if __name__ == "__main__":
	cal =  YearCalendar.objects.all()[0]
	
	scheds = cal.years_schedules()
	date = cal.start_date

	while (date <= date.today()):
		print(date)
		print(scheds[date])
		date += td(days=1)
		
