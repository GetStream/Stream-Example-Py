from django.conf.urls import include, url

from django.contrib import admin
from django.conf import settings
import core.views as views
from django.views.static import serve
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.trending, name='trending'),
    # the three feed pages
    url(r'^feed/$',
        views.feed, name='feed'),
    url(r'^aggregated_feed/$',
        views.aggregated_feed, name='aggregated_feed'),
    url(r'^notification_feed/$',
        views.notification_feed, name='notification_feed'),
    # a page showing the users profile
    url(r'^profile/(?P<username>[\w_-]+)/$',
        views.profile, name='profile'),
    # backends for follow and pin
    url(r'^pin/$',
        views.pin, name='pin'),
    url(r'^follow/$',
        views.follow, name='follow'),
    url(r'^people/$',
        views.people, name='people'),
    url(r'^auto_follow/$',
        views.auto_follow, name='auto_follow'),
    # the admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^robots.txt$', TemplateView.as_view(template_name='core/robots.txt',
                                              content_type="text/plain"))
]


urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include(
       'django.contrib.staticfiles.urls')),
] + urlpatterns
