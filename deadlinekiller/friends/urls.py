
from django.conf.urls import url

from . import views


urlpatterns = [


    url(r'^connections/$', views.Connections.as_view(), name='connections'),
    

]
