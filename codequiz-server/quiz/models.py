# -*- coding: utf-8 -*-

from django.db import models

from taggit_autosuggest.managers import TaggableManager


class Task(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    versionstring = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    body_xml = models.TextField()
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
        return ("T%03i:" % self.id) + self.title

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

    tasks = models.ManyToManyField(Task, through='TC_Membership')

    def __unicode__(self):
        return ("TC%03i:" % self.id) + self.title

    def LEN(self):
        return len(self.tc_membership_set.all())


class TC_Membership(models.Model):
    """
    This class specifies the association of a Task to a TaskCollection
    (needed for custom ordering of Tasks in TC)
    """

    task = models.ForeignKey(Task)
    group = models.ForeignKey(TaskCollection)
    ordering = models.FloatField()

