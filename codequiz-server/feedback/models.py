from django.db import models
from django.contrib.sites.models import Site
from quiz.models import Task
from django.utils.translation import ugettext as _


class Feedback(models.Model):
    site = models.ForeignKey(Site, verbose_name=_('site'))
    task = models.ForeignKey(Task)
    email = models.EmailField(blank=True, null=True, verbose_name=_('email'))
    text = models.TextField(verbose_name=_('text'))

    def __unicode__(self):
        feedback_lines = self.text.splitlines();
        dots = ""
        if len(feedback_lines) > 1:
            dots = " ..."
        return u'{task}: {text}'.format(task=self.task.title, text=self.text.splitlines()[0] + dots)
