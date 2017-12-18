
from django.conf.urls import url

from . import views


urlpatterns = [


    url(r'^connections/$', views.Connections.as_view(), name='connections'),
    # All friends
    url(r'^all/$', views.FriendsListView.as_view(), name='friends_list'),
    # Invitations
    url(r'^invitations/$', views.FriendsInvitationsView.as_view(), name='friends_invitations'),
    
    url(r'^make-connection/$', views.MakeConnectionView.as_view(), name='make_connection'),
    url(r'^delete-connection/(?P<pk>\d+)/$', views.DeleteConnectionView.as_view(), name='delete_connection'),


    
    

]
