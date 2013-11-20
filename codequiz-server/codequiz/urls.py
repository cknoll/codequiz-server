from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

import quiz.views as quiz_app_views

urlpatterns = patterns('',
                       #url(r'^$', quiz_app_views.index, name='index'), # Problems here
                       url(r'^quiz/', include('quiz.urls', namespace="quiz_ns")),
                       url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
                       url(r'^ratings/', include('ratings.urls')),
                       url(r'^feedback/', include('feedback.urls')),
                       # Examples:
                       # url(r'^$', 'codequiz.views.home', name='home'),
                       # url(r'^codequiz/', include('codequiz.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
)
