from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'core.views.trending',
                           name='trending'),
                       # the three feed pages
                       url(r'^feed/$',
                           'core.views.feed', name='feed'),
                       url(r'^aggregated_feed/$',
                           'core.views.aggregated_feed', name='aggregated_feed'),
                       url(r'^notification_feed/$',
                           'core.views.notification_feed', name='notification_feed'),
                       # a page showing the users profile
                       url(r'^profile/(?P<username>[\w_-]+)/$',
                           'core.views.profile', name='profile'),
                       # backends for follow and pin
                       url(r'^pin/$',
                           'core.views.pin', name='pin'),
                       url(r'^follow/$',
                           'core.views.follow', name='follow'),
                       url(r'^people/$',
                           'core.views.people', name='people'),
                       # the admin
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^auth/', include('django.contrib.auth.urls')),
                       )

if settings.DEBUG:
    urlpatterns = patterns('',
                           url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                           url(r'', include(
                               'django.contrib.staticfiles.urls')),
                           ) + urlpatterns
