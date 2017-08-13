from django.db import models
from quiz.models import Task
from django.utils.translation import ugettext as _
import datetime


class Feedback(models.Model):
    task = models.ForeignKey(Task)
    email = models.EmailField(blank=True, null=True, verbose_name=_('email'))
    text = models.TextField(verbose_name=_('text'))
    date = models.DateTimeField(default=datetime.datetime.now)
    answered = models.BooleanField(default=False, verbose_name=_('done'))

    def __unicode__(self):
        return '%s' % 'Feedback ' + str(self.id)
