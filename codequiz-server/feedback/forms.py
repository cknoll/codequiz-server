#!/usr/bin/env python
from django import forms
from django.contrib.sites.models import Site

from feedback.models import Feedback

class FeedbackForm(forms.ModelForm):
    """The form shown when giving feedback"""
    class Meta(object):
        model = Feedback
        exclude = ('date', 'answered')

# vim: et sw=4 sts=4
