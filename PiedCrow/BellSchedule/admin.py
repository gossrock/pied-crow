from django.contrib import admin

# Register your models here.

from .models import YearCalendar
from .models import SpecialDays
from .models import NormalScheduleRotation
from .models import Schedule
from .models import BellRing
from .models import Bell
from .models import RingPattern
from .models import RingPatternPart
from .models import EmergencyBells
from .models import EmergencyDrills




class SpecialDaysInline(admin.TabularInline):
    model = SpecialDays
    extra = 1
    
class NormalScheduleRotationInline(admin.TabularInline):
    model = NormalScheduleRotation
    extra = 1


class BellRingInline(admin.TabularInline):
    model = BellRing
    extra = 1

class RingPatternPartInline(admin.TabularInline):
    model = RingPatternPart
    extra = 1



class YearCalendarAdmin(admin.ModelAdmin):
	fields = ['name', 'start_date', 'end_date', 'sun_off', 'mon_off', 'tue_off', 'wed_off', 'thr_off', 'fri_off', 'sat_off']
	inlines = [NormalScheduleRotationInline, SpecialDaysInline]


class ScheduleAdmin(admin.ModelAdmin):
	fields = ['name']
	inlines = [BellRingInline]
	
class BellAdmin(admin.ModelAdmin):
	fields = ['name', 'gpio_pin']
	
class RingPatternAdmin(admin.ModelAdmin):
	fields = ['name', 'repeat']
	inlines = [RingPatternPartInline]

class EmergencyBellsAdmin(admin.ModelAdmin):
	fields = ['name', 'ring_pattern']
	
class EmergencyDrillsAdmin(admin.ModelAdmin):
	fields = ['name', 'emergency_bell', 'date', 'time']


admin.site.register(YearCalendar, YearCalendarAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Bell, BellAdmin)
admin.site.register(RingPattern, RingPatternAdmin)
admin.site.register(EmergencyBells, EmergencyBellsAdmin)
admin.site.register(EmergencyDrills, EmergencyDrillsAdmin)
