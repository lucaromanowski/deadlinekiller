from django.conf.urls import url

from . import views


urlpatterns = [
	
    url(r'^team-list/$', views.TeamListView.as_view(), name='team_list'),
    url(r'^team-detail/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.TeamDetailView.as_view(), name='team_detail'),
    url(r'^team-create/$', views.TeamCreateView.as_view(), name='team_create'),
    url(r'^team-delete/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.TeamDeleteView.as_view(), name='team_delete'),

    #Adding to the team and removing from the team (user profile)
    url(r'^team-add/$', views.AddToTheTeamView.as_view(), name='add_to_the_team'),
    

]