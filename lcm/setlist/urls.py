from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from lcm.setlist import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view()),
    url(r'^glance/(?P<year>\d+)/(?P<month>\d+)$', views.IndexView.as_view()),
    url(r'^sets/(?P<year>\d+)/(?P<month>\d+)$', views.SetsMonthView.as_view()),
    url(r'd3^$', views.dthreeView.as_view()),

    url(r'^api/owned$', views.OwnedSetList.as_view()),
    url(r'^api/owned/(?P<pk>[0-9]+)/$', views.OwnedSetDetail.as_view()),

    url(r'^api/by_chain$', views.OwnedSetChain.as_view()),
    url(r'^api/by_month$', views.OwnedSetMonth.as_view()),
    url(r'^api/by_theme$', views.OwnedSetTheme.as_view()),

)

urlpatterns = format_suffix_patterns(urlpatterns)
