from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.deadline_list, name='deadline_list'),
    url(r'^deadline-create/$', views.deadline_create, name='deadline_create'),
]
