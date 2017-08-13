# -*- coding: utf-8 -*-

from django.conf.urls import url
from quiz import views

urlpatterns = [url(r'^$', views.simple, kwargs={"template": "index.html"}, name='index'),
               url(r'^debug$', views.template_debug, name='debug'),
               url(r'^about$', views.simple, kwargs={"template": "about.html"}, name='about'),
               url(r'^test/run/', views.tc_run_view, name='tc_run_view'),
               url(r'^test/(?P<tc_id>\d+)/$', views.task_collection_view,
                   name='task_collection_view'),
               # view for showing a specific task outside of a tc
               # TODO: this should be restricted to moderators
               url(r'^explicit/(?P<task_id>\d+)/$', views.explicit_task_view,
                   name='explicit_task_view'),
               ]

# old advanced pattern:
# url(r'^test/result/(?P<tc_id>\d+)/(?P<tc_task_id>\d+)/$',
#                           views.tc_run_form_process, name='tc_run_form_process'),