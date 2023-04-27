from django.urls import include, re_path, path
from django.contrib import admin
import quiz.views as quiz_app_views
from django.shortcuts import redirect
admin.autodiscover()


urlpatterns = [re_path(r'^$', quiz_app_views.index, name='index'),
            re_path(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
            re_path(r'^quiz/', include(('quiz.urls', "quiz"), namespace="quiz_ns")),
            # temporarily excluded

            # re_path(r'^feedback/', include('feedback.urls')),

            # re_path(r'^polls/', include('polls.urls')), # from django example app

            # Examples:
            # re_path(r'^ratings/', include('ratings.urls')),
            # re_path(r'^$', 'codequiz.views.home', name='home'),
            # re_path(r'^codequiz/', include('codequiz.foo.urls')),

            # Uncomment the admin/doc line below to enable admin documentation:
            # re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

            # Uncomment the next line to enable the admin:
            # path('favicon.ico', lambda request: redirect('/static/favicon.ico', permanent=False)),
            path('admin/', admin.site.urls)
            # re_path(r'^admin/', include(admin.site.urls)),
            ]
