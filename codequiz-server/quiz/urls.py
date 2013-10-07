# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from quiz import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^task/view/(?P<task_id>\d+)/$', views.task_view, name='task_view'),
                       url(r'^test/run/(?P<tc_id>\d+)/(?P<tc_task_id>\d+)/$',
                           views.tc_run_view, name='tc_run_view'),
                       url(r'^test/result/(?P<tc_id>\d+)/(?P<tc_task_id>\d+)/$',
                           views.tc_run_form_process, name='tc_run_form_process'),
                       url(r'^test/(?P<tc_id>\d+)/$', views.task_collection_view, name='task_collection_view'),
                       url(r'^result/(?P<task_id>\d+)/$', views.form_result_view, name='task_form_process'),
                       #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
