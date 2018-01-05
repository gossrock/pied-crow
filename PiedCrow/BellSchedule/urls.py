from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import django.contrib.auth.urls

from PiedCrow import settings

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^alarms/$', views.view_alarms, name='view_alarms'),
    url(r'^alarms/start/(?P<emergency_type_id>[0-9]+)/$', views.start_alarm, name='start_alarm'),
    url(r'^alarms/stop/(?P<emergency_event_id>[0-9]+)/$', views.stop_alarm, name='stop_alarm'),
    url(r'^alarms/all_clear/(?P<emergency_event_id>[0-9]+)/$', views.all_clear_alarm, name='all_clear_alarm'),
    url(r'^schedule/(?P<sched_id>[0-9]+)/$', views.view_schedule, name='view_schedule'),
    url(r'^calendar/$', views.current_calendar, name='current_calendar'),
    url(r'^calendar/(?P<cal_id>[0-9]+)/$', views.calendar, name='calendar'),
    url(r'^js/clock.js$', views.clock_js, name='clock_js'),
    url(r'^data/bell_times.xml$', views.bell_times_xml, name='bell_times_xml'),
    url(r'^data/server_time$', views.server_time_text, name='server_time_text'),
    url('^accounts/login/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

