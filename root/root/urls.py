from django.conf.urls import patterns, include, url
from django.conf import settings



urlpatterns = patterns('',
    url(r'^wave/', include('wave.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
         'serve',
        {'document_root': settings.MEDIA_ROOT}),)
