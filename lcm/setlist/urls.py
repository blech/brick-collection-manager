from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from lcm.setlist import views

urlpatterns = patterns('',
    url(r'^api/legosets/$', views.LegoSetList.as_view()),
    url(r'^api/legosets/(?P<pk>[0-9]+)/$', views.LegoSetDetail.as_view()),

    url(r'^api/by_month/$', views.LegoSetMonth.as_view()),
    url(r'^api/by_chain/$', views.LegoSetChain.as_view()),

)

urlpatterns = format_suffix_patterns(urlpatterns)
