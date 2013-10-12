# -*- coding: utf-8 -*-
import datetime

from django.db import models

from taggit_autosuggest.managers import TaggableManager


class Task(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    revision = models.CharField(max_length=20)
    pub_date = models.DateTimeField('Publish date', default=datetime.datetime.now)
    body_xml = models.TextField('Body')
    tags = TaggableManager()

    def is_beta(self):
        tags = []
        for x in self.tags.names():
            tags.append(x)

        return 'beta' in tags

    #is_beta.admin_order_field = 'pub_date'
    is_beta.boolean = True
    is_beta.short_description = 'in beta state?'

    def __unicode__(self):
        return ("T%03i: " % self.id) + self.title

    def tags_as_string(self):
        """
        :return: all tags in one comma separated string
        """

        stringified = ", ".join([str(x) for x in self.tags.names()])
        return stringified


class TaskCollection(models.Model):
    """
    This is a Test (i.e. a collection of tasks)
    """
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    tags = TaggableManager()

    tasks = models.ManyToManyField(Task, through='TC_Membership')

    def __unicode__(self):
        return ("TC%03i:" % self.id) + self.title

    def number_of_tasks(self):
        return len(self.tc_membership_set.all())

    def tags_as_string(self):
        """
        :return: all tags in one comma separated string
        """

        stringified = ", ".join([str(x) for x in self.tags.names()])
        return stringified

class TC_Membership(models.Model):
    """
    This class specifies the association of a Task to a TaskCollection
    (needed for custom ordering of Tasks in TC)
    """

    task = models.ForeignKey(Task)
    group = models.ForeignKey(TaskCollection)
    ordering = models.FloatField()

# register model classes for django-generic-ratings
from ratings.handlers import ratings, RatingHandler
from ratings.forms import StarVoteForm


class CustomRatingHandler(RatingHandler):
    score_range = (0.5, 5)
    score_step = (0.5)
    can_delete_vote = False      # default is True
    form_class = StarVoteForm
    allow_anonymous = True       # default is False
    votes_per_ip_address = 0     # default is 0, meaning unlimited
    cookie_max_age = 2592000     # 30 days in seconds, default is 1 year

    def allow_key(self, request, instance, key):
        return key in ('difficulty', 'quality')


ratings.register(Task, CustomRatingHandler)
