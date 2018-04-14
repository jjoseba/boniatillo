from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    url(r'^activities/$', views.activity_list, name='activity_list'),
    #url(r'^categories/add$', views.add_user_activity, name='add_category'),
    #url(r'^categories/add$', views.user_activity, name='add_category'),

]