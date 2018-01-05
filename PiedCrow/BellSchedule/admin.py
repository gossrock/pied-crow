from django.contrib import admin

# Register your models here.

from .models import YearCalendar
from .models import SpecialDay
from .models import NormalScheduleRotation
from .models import Schedule
from .models import BellRing
from .models import RingPattern
from .models import RingPatternPart

from .models import EmergencyType





class SpecialDayInline(admin.TabularInline):
    model = SpecialDay
    extra = 1
    ordering = ('date',)
    
class NormalScheduleRotationInline(admin.TabularInline):
    model = NormalScheduleRotation
    extra = 1


class BellRingInline(admin.TabularInline):
    model = BellRing
    extra = 1
    ordering = ('time',)

class RingPatternPartInline(admin.TabularInline):
    model = RingPatternPart
    extra = 1



class YearCalendarAdmin(admin.ModelAdmin):
	fields = ['name', 'start_date', 'end_date', 'sun_off', 'mon_off', 'tue_off', 'wed_off', 'thr_off', 'fri_off', 'sat_off']
	inlines = [NormalScheduleRotationInline, SpecialDayInline]


class ScheduleAdmin(admin.ModelAdmin):
	fields = ['name']
	inlines = [BellRingInline]
	

	
class RingPatternAdmin(admin.ModelAdmin):
	fields = ['name', 'repeat']
	inlines = [RingPatternPartInline]

class EmergencyTypeAdmin(admin.ModelAdmin):
	fields = ['name', 'ring_pattern', 'all_clear_pattern']
	



admin.site.register(YearCalendar, YearCalendarAdmin)
admin.site.register(Schedule, ScheduleAdmin)

admin.site.register(RingPattern, RingPatternAdmin)
admin.site.register(EmergencyType, EmergencyTypeAdmin)
