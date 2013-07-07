# -*- coding: utf-8 -*-

from django.db import models

class Task(models.Model):

    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    versionstring = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    body_xml = models.TextField()
    tag_list = models.TextField()# separator : "; "

    def is_beta(self):
        return 'beta' in self.tag_list.split("; ")

    #is_beta.admin_order_field = 'pub_date'
    is_beta.boolean = True
    is_beta.short_description = 'in beta state?'

    def __unicode__(self):
        return ("T%03i:" % self.id) +self.title

class TaskCollection(models.Model):
    """
    This is a Test (i.e. a collection of tasks)
    """
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    tasks = models.ManyToManyField(Task, through='TC_Membership')

    def __unicode__(self):
        return ("TC%03i:" % self.id) +self.title


class TC_Membership(models.Model):
    """
    This class specifies the assoziation of a Task to a TaskCollection
    (needed for custom ordering of Tasks in TC)
    """

    task = models.ForeignKey(Task)
    group = models.ForeignKey(TaskCollection)
    ordering = models.FloatField()

