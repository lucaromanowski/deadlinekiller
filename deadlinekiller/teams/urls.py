from django.conf.urls import url

from . import views


urlpatterns = [
    
    url(r'^team-list/$', views.TeamList.as_view(), name='team_list'),
    

]