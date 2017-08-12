from django.conf.urls import url

from feedback.views import FeedbackView

# extract parts of the URL to kwargs (first all digits until "/" as the task_id and the remainder into an URL)
urlpatterns = [url(r'^ajax/(?P<task>\d+)/(?P<url>.*)$', FeedbackView.as_view(), name='feedback'),
               ]

