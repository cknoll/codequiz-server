from django.urls import re_path
from quiz import views

urlpatterns = [re_path(r'^$', views.simple, kwargs={"template": "index.html"}, name='index'),
               re_path(r'^debug$', views.template_debug, name='debug'),
               re_path(r'^about$', views.simple, kwargs={"template": "about.html"}, name='about'),
               re_path(r'^test/run/', views.tc_run_view, name='tc_run_view'),
               re_path(r'^test/(?P<tc_id>\d+)/$', views.task_collection_view,
                   name='task_collection_view'),
               # view for showing a specific task outside of a tc
               # TODO: this should be restricted to moderators
               re_path(r'^explicit/(?P<task_id>\d+)/$', views.explicit_task_view,
                   name='explicit_task_view'),
               re_path(r'^backup$', views.download_backup_fixtures, name='download_backup_fixtures'),
               ]

# old advanced pattern:
# re_path(r'^test/result/(?P<tc_id>\d+)/(?P<tc_task_id>\d+)/$',
#                           views.tc_run_form_process, name='tc_run_form_process'),
