# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from quiz import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^task/(?P<task_id>\d+)/$', views.task_view, name='task_view'),
    url(r'^result/(?P<task_id>\d+)/$', views.form_result_view, name='task_form_process'),
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
