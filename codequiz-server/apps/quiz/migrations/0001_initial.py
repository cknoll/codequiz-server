# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-13 20:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('hash', models.CharField(max_length=128)),
                ('log', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TaggedModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TC_Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('taggedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.TaggedModel')),
                ('author', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('revision', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Publish date')),
                ('body_data', models.TextField(db_column=b'body_xml', verbose_name=b'Body')),
                ('tags', taggit_autosuggest.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            bases=('quiz.taggedmodel',),
        ),
        migrations.CreateModel(
            name='TaskCollection',
            fields=[
                ('taggedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.TaggedModel')),
                ('author', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('exam_mode', models.IntegerField(choices=[(0, b'No Exam'), (1, b'No Solutions, only Right/Wrong'), (2, b'No Results, just continue quiz')], default=0)),
                ('tags', taggit_autosuggest.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            bases=('quiz.taggedmodel',),
        ),
        migrations.AddField(
            model_name='tc_membership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.TaskCollection'),
        ),
        migrations.AddField(
            model_name='tc_membership',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Task'),
        ),
        migrations.AddField(
            model_name='taskcollection',
            name='tasks',
            field=models.ManyToManyField(through='quiz.TC_Membership', to='quiz.Task'),
        ),
    ]