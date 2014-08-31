from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from lcm.setlist import views

urlpatterns = patterns('',
    url(r'^legosets/$', views.LegoSetList.as_view()),
    url(r'^legosets/(?P<pk>[0-9]+)/$', views.LegoSetDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
