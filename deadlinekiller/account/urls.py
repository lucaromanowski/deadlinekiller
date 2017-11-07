from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    #url(r'^login/$', views.user_login, name='login'),
    
    # Login view
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    # Logout view
    url(r'^logout/$',  auth_views.LogoutView.as_view(), name='logout'),
    # Logout then login
    url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_than_login'),



    # TEST URL
    url(r'^test-home/$', views.test_home, name='test_home'),
]
