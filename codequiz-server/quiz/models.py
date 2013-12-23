# -*- coding: utf-8 -*-
import datetime

from django.db import models

from taggit_autosuggest.managers import TaggableManager
from django.core.urlresolvers import reverse


class TaggedModel:
    def __unicode__(self):
        return ("T%03i: " % self.id) + self.title

    def tags_as_string(self):
        """
        get all tags in one comma separated string

        @return: all tags in one comma separated string
        """
        return ", ".join([str(x) for x in self.tags.names()])


class Task(models.Model, TaggedModel):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    revision = models.IntegerField(default=0)
    pub_date = models.DateTimeField('Publish date', default=datetime.datetime.now)
    body_data = models.TextField('Body', db_column='body_xml')
    tags = TaggableManager(blank=True)

    def get_absolute_url(self):
        return reverse('quiz_ns:task_view', args=[str(self.id)])


class QuizResult(models.Model):
    date = models.DateTimeField()
    hash = models.CharField(max_length=128)
    log = models.TextField()


class TaskCollection(models.Model, TaggedModel):
    """
    This is a Test (i.e. a collection of tasks)
    """
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    tags = TaggableManager(blank=True)
    EXAM_MODE_NONE = 0
    EXAM_MODE_NO_SOLUTIONS = 1
    EXAM_MODE_NO_RESULTS = 2
    EXAM_MODE_CHOICES = (
        (EXAM_MODE_NONE, 'No Exam'),
        (EXAM_MODE_NO_SOLUTIONS, 'No Solutions, only Right/Wrong'),
        (EXAM_MODE_NO_RESULTS, 'No Results, just continue quiz'),
    )
    exam_mode = models.IntegerField(max_length=1,
                                    choices=EXAM_MODE_CHOICES,
                                    default=EXAM_MODE_NONE)

    tasks = models.ManyToManyField(Task, through='TC_Membership')

    def number_of_tasks(self):
        return self.tasks.count()

    def should_give_solution(self):
        return self.exam_mode in (self.EXAM_MODE_NONE,)

    def should_give_feedback(self):
        return self.exam_mode in (self.EXAM_MODE_NONE, self.EXAM_MODE_NO_SOLUTIONS)


class TC_Membership(models.Model):
    """
    This class specifies the association of a Task to a TaskCollection
    (needed for custom ordering of Tasks in TC)
    """

    task = models.ForeignKey(Task)
    group = models.ForeignKey(TaskCollection)
    ordering = models.PositiveIntegerField()

# register model classes for django-generic-ratings
from ratings.handlers import ratings, RatingHandler
from ratings.forms import StarVoteForm


class CustomRatingHandler(RatingHandler):
    score_range = (0.5, 5)
    score_step = 0.5
    can_delete_vote = False      # default is True
    form_class = StarVoteForm
    allow_anonymous = True       # default is False
    votes_per_ip_address = 0     # default is 0, meaning unlimited
    cookie_max_age = 2592000     # 30 days in seconds, default is 1 year

    def allow_key(self, request, instance, key):
        return key in ('difficulty', 'quality')


ratings.register(Task, CustomRatingHandler)
