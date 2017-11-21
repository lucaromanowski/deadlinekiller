from django.conf.urls import url

from . import views


urlpatterns = [
	# Deadline CRUD

	# List view
    url(r'^$', views.deadline_list, name='deadline_list'),

    # Detail view
    url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$', views.deadline_detail, name='deadline_detail'),

    # Create
    url(r'^deadline-create/$', views.deadline_create, name='deadline_create'),

    # Update
    url(r'^deadline-update/(?P<pk>\d+)/(?P<slug>[-\w]+)/$', views.deadline_update, name='deadline_update'),

   
]
