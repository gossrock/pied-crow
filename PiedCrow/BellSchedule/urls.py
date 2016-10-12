from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from PiedCrow import settings

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^js/clock.js$', views.clock_js, name='clock_js'),
    url(r'^data/bell_times.xml$', views.bell_times_xml, name='bell_times_xml'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

