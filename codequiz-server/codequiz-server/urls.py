from django.conf.urls import include, url
from django.contrib import admin

import quiz.views as quiz_app_views

from django.contrib import admin
admin.autodiscover()


urlpatterns = [url(r'^$', quiz_app_views.index, name='index'),
               url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
               url(r'^quiz/', include('quiz.urls', namespace="quiz_ns")),
               # temporarily excluded

               # url(r'^feedback/', include('feedback.urls')),

               # url(r'^polls/', include('polls.urls')), # from django example app

               # Examples:
               # url(r'^ratings/', include('ratings.urls')),
               # url(r'^$', 'codequiz.views.home', name='home'),
               # url(r'^codequiz/', include('codequiz.foo.urls')),

               # Uncomment the admin/doc line below to enable admin documentation:
               # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

               # Uncomment the next line to enable the admin:
               url(r'^admin/', include(admin.site.urls)),
               ]
