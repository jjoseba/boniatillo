from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    url(r'^activities/$', views.activity_list, name='activity_list'),
    url(r'^activities/add$', views.add_activity, name='add_activity'),
    url(r'^activity_detail/', views.activity_detail, name='activity_detail'),

]