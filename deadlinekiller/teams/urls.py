from django.conf.urls import url

from . import views


urlpatterns = [
	
    url(r'^team-list/$', views.TeamListView.as_view(), name='team_list'),
    url(r'^team-detail/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.TeamDetailView.as_view(), name='team_detail'),
    url(r'^team-create/$', views.TeamCreateView.as_view(), name='team_create'),
    

]