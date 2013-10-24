from django.db import models
from quiz.models import Task
from django.utils.translation import ugettext as _


class Feedback(models.Model):
    task = models.ForeignKey(Task)
    email = models.EmailField(blank=True, null=True, verbose_name=_('email'))
    text = models.TextField(verbose_name=_('text'))

    def __unicode__(self):
        feedback_lines = self.text.splitlines()
        dots = ""
        if len(feedback_lines) > 1:
            dots = " ..."
        return u'{task}: {text}'.format(task=self.task.title, text=feedback_lines[0] + dots)
